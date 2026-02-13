"""
Read packets from a Chapter 10 file, apply optional filters, and pass them to a provided data sink function.
"""

from threading import Event
from chapter10 import C10

__all__ = ['parse_file', 'terminate']

_channel_types = []
_channel_ids = []

terminate = Event()

def parse_file(
        channel_ids_filter : list, 
        channel_types_filter : list, 
        infile : str, 
        data_sink_func : function
        ):
    """Main entry point for parsing a Chapter 10 file.
    
    :param args: The argparse.Namespace object containing CLI arguments.
    """
    _set_filter_parameters(channel_ids_filter, channel_types_filter)
    _read_packets(infile, data_sink_func)


def _set_filter_parameters(ids, types):
    """
    Set the filter parameters for channel IDs and types. These parameters will be used to determine which packets to process.
    
    :param ids: List of channel IDs to include in processing.
    :param types: List of channel types to include in processing.
    """
    global _channel_types, _channel_ids

    _channel_types.clear()
    _channel_ids.clear()

    if ids:
        _channel_ids.extend(ids)
    
    if types:
        _channel_types.extend(types)

    if (type(_channel_types) == type(types)):
        _channel_types = types
    
    
def _read_packets(infile, sink):
    global terminate
    
    for packet in C10(infile):
        
        if terminate.is_set():
            # perform any per-thread cleanup here if needed
            break

        if (_passes_filter(packet.channel_id, packet.data_type)):
            sink([packet])
        else:
            continue


def _passes_filter(id, type):
    """Returns False if id or type are not in their respective [non-empty] filter lists."""
    global _channel_types, _channel_ids

    if (len(_channel_ids) > 0 and id not in _channel_ids):
        return False
    
    if (len(_channel_types) > 0 and type not in _channel_types):
        return False
    
    return True


