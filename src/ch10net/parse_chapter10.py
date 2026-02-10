from queue import *
from threading import Event
from chapter10 import C10

__all__ = ['parse_file', 'read_packets','terminate_event']

channel_types = {} 
channel_ids = {}

q = Queue(maxsize=10000)

terminate_event = Event()


def parse_file(args):
    """Main entry point for parsing a Chapter 10 file.
    
    :param args: The argparse.Namespace object containing CLI arguments.
    """
    set_filter_parameters(args.channel_ids, args.channel_types)
    read_packets(args.infile)


def set_filter_parameters(ids, types):
    """
    Set the filter parameters for channel IDs and types. These parameters will be used to determine which packets to process.
    
    :param ids: List of channel IDs to include in processing.
    :param types: List of channel types to include in processing.
    """
    if (type(channel_ids) == type(ids)):
        channel_ids = ids

    if (type(channel_types) == type(types)):
        channel_types = types
    
    
def read_packets(infile):
    for packet in C10(infile):
        # Check for termination request regularly so threads can exit cleanly.
        if terminate_event.is_set():
            # perform any per-thread cleanup here if needed
            break

        if (not passes_filter(packet.channel_id, packet.data_type)):
            continue

        time = packet.get_time()
        data = packet.__bytes__()
        length = len(data)
        

def passes_filter(id, type):
    """Returns False if id or type are not in their respective [non-empty] filter lists."""
    if (len(channel_ids) > 0 and id not in channel_ids):
        return False
    
    if (len(channel_types) > 0 and type not in channel_types):
        return False
    
    return True


def retreive_packets():
    """Generator that yields packets from the internal queue."""
    while not terminate_event.is_set():
        try:
            packet = q.get(timeout=1)  # Adjust timeout as needed
            yield packet
        except Empty:
            continue
