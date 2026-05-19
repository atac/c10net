"""
Takes parsed Chapter 10 packets, generates appropriate UDP transfer headers, 
and writes them toa PCAP file.
"""

from collections.abc import Callable

from queue import ShutDown

from c10net.functions.ethernet_packet_generator import EthernetGenerator
from c10net.tasks.stage import Stage

#__all__ = ['build_ethernet_packets', 'deposit_chapter10_packets', 'terminate', 'finish']


class Chapter10ToEthernet(Stage):
    def __init__(self, cli_args : dict, source : Callable = None, direct_link : Callable = None):
        super().__init__(source, direct_link)
        self._eth_gen = EthernetGenerator(cli_args)
        self._have_time = False
        self._pre_time_buffer = []

        self._debug_count = 0

    def start(self):
        self._build_ethernet_packets()

    def _build_ethernet_packets(self):
        """Continuously poll the DataPipe for Chapter 10 packets, generate 
        Ethernet packets, and pass to the provided data sink function."""

        try:
            while not self._state.terminate.is_set():
                ch10_packets = self.retrieve()
                self._process(ch10_packets)
        except ShutDown:
            pass

        self._pipe.shutdown(immediate=self._state.terminate.is_set())


    def _process(self, packets : list):
            out_data = []

            for p in packets:
                if self._have_time:
                    eth_packets = self._eth_gen.generate_from_chapter10(p)
                    out_data.extend(eth_packets)
                else:
                    self._have_time = self._handle_pre_time_packet(p, out_data)
            
            self.deposit(out_data)
            self._debug_count += len(out_data)

    def _handle_pre_time_packet(self, packet, out_data):
        """Handle a Chapter 10 packet that does not have an associated timestamp.
        This function is used to assign a timestamp to packets based on the next
        packet that has a timestamp."""
        if (not (packet.parent and packet.parent.last_time is not None)):
            self._pre_time_buffer.append(packet)
            return False
        
        for p in self._pre_time_buffer:
            p.parent.last_time = packet.parent.last_time
            eth_packets = self._eth_gen.generate_from_chapter10(p)
            out_data.extend(eth_packets)
        self._pre_time_buffer = []

        return True

    def pipe_output(self):
        return self._pipe.retrieve
    
    def direct_input(self):
        return self._process