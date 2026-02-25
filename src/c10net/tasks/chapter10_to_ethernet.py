"""
Takes parsed Chapter 10 packets, generates appropriate UDP transfer headers, 
and writes them toa PCAP file.
"""

from collections.abc import Callable
from threading import Event

from tasks.data_pipe import DataPipe
from functions.ethernet_packet_generator import EthernetGenerator

__all__ = ['build_ethernet_packets', 'deposit_chapter10_packets', 'terminate', 'finish']

terminate = Event()
finish = Event()
_pipe = DataPipe(terminate)

def build_ethernet_packets(cli_args, data_sink_func : Callable):
    """Continuously poll the DataPipe for Chapter 10 packets, generate 
    Ethernet packets, and pass to the provided data sink function."""
    global terminate, _pipe
    eth_gen = EthernetGenerator(cli_args)

    have_time = False

    while not terminate.is_set():
        if (finish.is_set() and _pipe.is_empty()):
            break
        
        ch10_packets = _pipe.retrieve()

        out_data = []

        for packet in ch10_packets:
            if have_time:
                eth_packets = eth_gen.generate_from_chapter10(packet)
                out_data.extend(eth_packets)
            else:
                have_time = _handle_pre_time_packet(packet, eth_gen, out_data)
        
        data_sink_func(out_data)


_pre_time_buffer = []

def _handle_pre_time_packet(packet, ethernet_generator, out_data):
    """Handle a Chapter 10 packet that does not have an associated timestamp.
    This function is used to assign a timestamp to packets based on the next
    packet that has a timestamp."""
    global _pre_time_buffer

    if (not (packet.parent and packet.parent.last_time is not None)):
        pre_time_buffer.append(packet)
        return False
    
    for p in pre_time_buffer:
        p.parent.last_time = packet.parent.last_time
        eth_packets = ethernet_generator.generate_from_chapter10(p)
        out_data.extend(eth_packets)
    pre_time_buffer = []

    return True


def deposit_chapter10_packets(packets):
    global _pipe
    _pipe.deposit(packets)