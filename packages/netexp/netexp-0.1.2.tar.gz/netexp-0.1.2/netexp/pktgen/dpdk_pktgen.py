
import ipaddress
import time

from netexp.helpers import get_ssh_client, remote_command, \
    run_console_commands, watch_command


class DpdkPktgen:
    """Wrapper for DPDK pktgen.

    Attributes:
        pktgen_server: The remote to run pktgen on.
        remote_cmd: The command to be run to start DPDK pktgen.
    """
    def __init__(self, pktgen_server: str, remote_cmd: str):
        self.pktgen_ssh_client = get_ssh_client(pktgen_server)
        self.pktgen = remote_command(self.pktgen_ssh_client, remote_cmd,
                                     pty=True)
        self.remote_cmd = remote_cmd

    def wait_until_ready(self):
        watch_command(self.pktgen, keyboard_int=self.pktgen.close,
                      stop_pattern='## Done ##')

    def commands(self, cmds, timeout: float = 0.5):
        run_console_commands(self.pktgen, cmds, timeout=timeout,
                             console_pattern='\r\nPktgen:/> ')

    def config(self, nb_src: int, nb_dest: int, nb_pkts: int, pkt_size: int,
               init_ip, init_port: int):
        max_src_ip = ipaddress.ip_address(init_ip) + nb_src - 1
        max_dst_ip = ipaddress.ip_address(init_ip) + nb_dest - 1

        commands = [
            f'set 0 count {nb_pkts}',
            f'range 0 dst port start {init_port}',
            f'range 0 src ip max {max_src_ip}',
            f'range 0 dst ip max {max_dst_ip}',
            f'range 0 size start {pkt_size}',
            f'range 0 size min {pkt_size}',
            f'range 0 size max {pkt_size}',
        ]
        self.commands(commands)

    def config_pcap

    def start(self, rate):
        commands = [
            f'set 0 rate {rate}',
            'start 0',
        ]
        self.commands(commands)

    def clear(self):
        self.commands('clr')

    def close(self):
        self.pktgen.send('quit\n')
        time.sleep(0.1)
        self.pktgen_ssh_client.close()

    def get_nb_sent_pkts(self):
        self.pktgen.get_nb_sent_pkts()
        self.pktgen.send(
            'lua \'print(pktgen.portStats("all", "port")[0].opackets)\'\n')
        output = watch_command(
            self.pktgen, keyboard_int=lambda: self.pktgen.send('\x03'),
            stop_pattern='\r\n\\d+\r\n'
        )
        lines = output.split('\r\n')
        lines = [ln for ln in lines if ln.isdigit()]
        return int(lines[-1])

    def get_tx_rate(self):
        # TODO(sadok): Not sure if there is a way to check the TX rate here.
        return 0
