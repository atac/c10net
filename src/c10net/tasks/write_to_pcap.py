"""
Polls the DataPipe for Ethernet packets and writes them to a PCAP file using
Scapy's PcapWriter.
"""

from collections.abc import Callable
from threading import Event

from scapy.all import PcapWriter

from .stage import Stage

class WritePcap(Stage):
    def __init__(self, out_pathname : str):
        super().__init__(sink=None)
        self._writer = PcapWriter(out_pathname, append=False)

    def start(self):
        while not self._state.terminate.is_set():
            if (self._state.finish.is_set() and self._pipe.is_empty()):
                break

            eth_packets = self._pipe.retrieve()
            self._process(eth_packets)

        self._writer.close()
    
    def _process(self, eth_packets : list):
        self._writer.write(eth_packets)
        self._writer.flush()

    def pipe_input(self):
        return self._pipe.deposit
    
    def direct_input(self):
        return self._process