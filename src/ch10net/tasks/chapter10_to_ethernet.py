"""
Takes parsed Chapter 10 packets, generates appropriate UDP transfer headers, 
and writes them toa PCAP file.
"""

from threading import Event

from task_data_pipe import DataPipe
from ch10net.functions.ethernet_packet_generator import EthernetGenerator

__all__ = ['build_ethernet_packets', 'deposit_chapter10_packets', 'terminate', 'finish']

terminate = Event()
finish = Event()
_pipe = DataPipe(terminate)

def build_ethernet_packets(cli_args, data_sink_func : function):
    """Continuously poll the DataPipe for Chapter 10 packets, generate 
    Ethernet packets, and pass to the provided data sink function."""
    global terminate, _pipe
    eth_gen = EthernetGenerator(cli_args)

    while not terminate.is_set():
        if (finish.is_set() and _pipe.is_empty()):
            break
        
        ch10_packets = _pipe.retrieve()

        out_data = []

        for packet in ch10_packets:
            eth_packets = eth_gen.generate_from_chapter10(packet)
            out_data.append(eth_packets)
        
        data_sink_func(out_data)



def deposit_chapter10_packets(packets):
    global _pipe
    _pipe.deposit(packets)