"""
Read packets from a Chapter 10 file, apply optional filters, and pass
them to the internal DataPipe
"""
import os
from collections.abc import Callable
from queue import ShutDown

from chapter10 import C10, Packet

from c10net.functions.packet_pulser import PacketPulser
from .stage import Stage


class ParseChapter10(Stage):

    #__all__ = ['parse_file', 'terminate']

    def __init__(
            self, 
            infile : str, 
            channel_ids : list = None,
            channel_types : list = None,
            pass_setup_packet : bool = False,
            pulse_interval : float = 0.0,
            direct_link : Callable = None
            ):
        '''
        Initializer for the ParseChapter10 stage.

        :param infile: Pathname for the input Chapter 10 file
        :param channel_ids: List of channel IDs to process (empty or None to allow all)
        :param channel_types: List of channel types to process (empty or None to allow all)
        :param pass_setup_packet: When set, allows the setup packet to pass the filter
        :param pulse_interval: When non-zero, pulses the setup packet at the given interval (in seconds)
        :param pipe_link: A function linking stages in the pipeline
        '''
        super().__init__(direct_link=direct_link)
        
        self._infile = infile
        self._channel_types = channel_types
        self._channel_ids = channel_ids
        self._pass_setup_packet = pass_setup_packet

        self._pulser = None
        
        if (pulse_interval > 0.0):
            self._pulser = PacketPulser()
            self._pulser.set_interval(pulse_interval)

        self._debug_count = 0

    def start(self):
        self._read_packets(self._infile)

    def _read_packets(self, infile):
        """Iterates through packets of a Chapter 10 file, passing them to the pipe."""
        
        file_pos = 0.0
        size = os.path.getsize(infile)

        try:
            for packet in C10(infile):
                file_pos += packet.packet_length
                self._state.set_progress(file_pos / size)
                
                if self._state.terminate.is_set():
                    break
                
                self._process(packet)
        except ShutDown:
            pass
        
        self._pipe.shutdown(immediate=self._state.terminate.is_set())
    
    def _process(self, packet : Packet):
        # do pulse processing if pulser is set up
        if (not self._pulser is None):
            if (packet.channel_id == 0 and packet.data_type == 0x01):
                self._pulser.set_packet(packet)

            pulse_packet = self._pulser.check_pulse()

            if (not pulse_packet is None):
                print(pulse_packet)
                self.deposit([pulse_packet])
                self._debug_count += 1

        if (self._passes_filter(packet.channel_id, packet.data_type)):
            self.deposit([packet])

        self._debug_count += 1

    def _passes_filter(self, id, type):
        """Returns False if id or type are not in their respective [non-empty] filter lists."""
        ids = self._channel_ids
        types = self._channel_types

        if (self._pass_setup_packet and id == 0 and type == 1):
            return True

        if (ids and len(ids) > 0 and id not in ids):
            return False
        
        if (types and len(types) > 0 and type not in types):
            return False
        
        return True

    def pipe_output(self):
        return self._pipe.retrieve