
import os
import re
import subprocess
import sys
import time

import paramiko


# from here: https://stackoverflow.com/a/287944/2027390
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def remote_command(client, command, pty=False, print_command=False):
    transport = client.get_transport()
    session = transport.open_session()

    if pty:
        session.setblocking(0)
        session.get_pty()

    session.exec_command(command)

    if print_command:
        print(f'exp command: {command}')

    return session


def upload_file(host, local_path, remote_path):
    subprocess.run(['scp', '-r', local_path, f'{host}:{remote_path}'])


def download_file(host, remote_path, local_path):
    subprocess.run(['scp', '-r', f'{host}:{remote_path}', local_path])


def remove_remote_file(host, remote_path):
    subprocess.run(['ssh', host, 'rm', remote_path])


def watch_command(command, stop_condition=None, keyboard_int=None,
                  timeout=None, stdout=True, stderr=True, stop_pattern=None,
                  max_match_length=1024):
    if stop_condition is None:
        stop_condition = command.exit_status_ready

    if timeout is not None:
        deadline = time.time() + timeout

    output = ''

    def continue_running():
        if (stop_pattern is not None):
            search_len = min(len(output), max_match_length)
            if re.search(stop_pattern, output[-search_len:]):
                return False
        return not stop_condition()

    try:
        while continue_running():
            time.sleep(0.01)

            if command.recv_ready():
                data = command.recv(512)
                decoded_data = data.decode('utf-8')
                output += decoded_data
                if stdout:
                    sys.stdout.write(decoded_data)
                    sys.stdout.flush()

            if command.recv_stderr_ready():
                data = command.recv_stderr(512)
                decoded_data = data.decode('utf-8')
                output += decoded_data
                if stderr:
                    sys.stderr.write(decoded_data)
                    sys.stderr.flush()

            if (timeout is not None) and (time.time() > deadline):
                break
    except KeyboardInterrupt:
        if keyboard_int is None:
            raise
        keyboard_int()
        raise

    return output


def get_ssh_client(host, nb_retries=0, retry_interval=1):
    # adapted from https://gist.github.com/acdha/6064215
    client = paramiko.SSHClient()
    client._policy = paramiko.WarningPolicy()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)

    cfg = {'hostname': host}

    user_config = ssh_config.lookup(host)

    for k in ('hostname', 'username', 'port'):
        if k in user_config:
            cfg[k] = user_config[k]

    if 'user' in user_config:
        cfg['username'] = user_config['user']

    if 'proxycommand' in user_config:
        cfg['sock'] = paramiko.ProxyCommand(user_config['proxycommand'])

    if 'identityfile' in user_config:
        cfg['pkey'] = paramiko.RSAKey.from_private_key_file(
                        user_config['identityfile'][0])

    trial = 0
    while True:
        if trial > nb_retries:
            raise paramiko.ssh_exception.NoValidConnectionsError
        trial += 1
        try:
            client.connect(**cfg)
            break
        except KeyboardInterrupt as e:
            raise e
        except:
            time.sleep(retry_interval)
            continue

    return client


def run_console_commands(console, commands, timeout=1, console_pattern=None):
    if not isinstance(commands, list):
        commands = [commands]

    if console_pattern is not None:
        console_pattern_len = len(console_pattern)
    else:
        console_pattern_len = None

    for cmd in commands:
        console.send(cmd + '\n')
        watch_command(console, keyboard_int=lambda: console.send('\x03'),
                      timeout=timeout, stop_pattern=console_pattern,
                      max_match_length=console_pattern_len)
