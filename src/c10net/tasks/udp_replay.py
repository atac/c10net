from collections.abc import Callable
from queue import ShutDown
import time

from scapy.all import *
from .stage import Stage

class UdpReplay(Stage):
    def __init__(self, source : Callable = None):
        super().__init__(source=source)

        self._first_real_time = None
        self._first_file_time = None

        self._debug_count = 0

    def start(self):
        try:
            while not self._state.terminate.is_set():
                eth_packets = self.retrieve()
                self._replay_packets(eth_packets)
        except ShutDown:
            pass

        self._pipe.shutdown(immediate=self._state.terminate.is_set())

    def _replay_packets(self, eth_packets : list):
        print (len(eth_packets))
        for packet in eth_packets:
            self._replay(packet)

            if (self._state.terminate.is_set()):
                break

    def _replay(self, ethernet_packet):
        # Calculate the time delay from the previous packet's timestamp to the current packet's timestamp
        #if (not self._first_real_time or not self._first_file_time):
        #    self._first_real_time = time.time()
        #    self._first_file_time = ethernet_packet.time

        #real_offset = time.time() - self._first_real_time
        #file_offset = ethernet_packet.time - self._first_file_time

        #delay = file_offset - real_offset

        #if (delay >= 0.0):
            # Wait for the calculated delay (relative to the previous packet)
            #time.sleep(float(delay))
        #    pass

        # Send the packet over the network
        send(ethernet_packet.payload, verbose=False)

        self._debug_count += 1
    

    def direct_input(self):
        return self._replay_packets
