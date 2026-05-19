"""
Polls the DataPipe for Ethernet packets and writes them to a PCAP file using
Scapy's PcapWriter.
"""

from collections.abc import Callable
from threading import Event

from queue import ShutDown

from scapy.all import PcapWriter

from .stage import Stage

class WritePcap(Stage):
    def __init__(self, out_pathname : str, source : Callable = None):
        super().__init__(source=source)
        self._writer = PcapWriter(out_pathname, append=False)
        
        self._debug_count = 0

    def start(self):
        try:
            while not self._state.terminate.is_set():
                eth_packets = self.retrieve()
                self._process(eth_packets)
        except ShutDown:
            pass

        self._pipe.shutdown(immediate=self._state.terminate.is_set())

        self._writer.close()
    
    def _process(self, eth_packets : list):
        self._writer.write(eth_packets)
        self._writer.flush()
        
        self._debug_count += len(eth_packets)
    
    def direct_input(self):
        return self._process