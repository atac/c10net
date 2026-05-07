"""
Read packets from a Chapter 10 file, apply optional filters, and pass
them to the internal DataPipe
"""
import os
from collections.abc import Callable

from chapter10 import C10, Packet

from .stage import Stage


class ParseChapter10(Stage):

    #__all__ = ['parse_file', 'terminate']

    def __init__(
            self, 
            infile : str, 
            channel_ids : list = None,
            channel_types : list = None,
            pass_setup_packet : bool = False,
            sink : Callable = None
            ):
        '''
        Initializer for the ParseChapter10 stage.

        :param infile: Pathname for the input Chapter 10 file
        :param channel_ids: List of channel IDs to process (empty or None to allow all)
        :param channel_types: List of channel types to process (empty or None to allow all)
        :param pass_setup_packet: When set, allows the setup packet to pass the filter
        :param sink: Callable deposit method of a DataPipe
        '''
        super().__init__(sink)
        
        self._infile = infile
        self._channel_types = channel_types
        self._channel_ids = channel_ids
        self._pass_setup_packet = pass_setup_packet

    def start(self):
        self._read_packets(self._infile)

    def _read_packets(self, infile):
        """Iterates through packets of a Chapter 10 file, passing them to the pipe."""
        
        file_pos = 0.0
        size = os.path.getsize(infile)

        for packet in C10(infile):
            file_pos += packet.packet_length
            self._state.set_progress(file_pos / size)
            
            if self._state.terminate.is_set() or self._state.finish.is_set():
                # No cleanup needed
                break

            self._process(packet)
    
    def _process(self, packet : Packet):
        if (self._passes_filter(packet.channel_id, packet.data_type)):
            self._deposit([packet])

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

