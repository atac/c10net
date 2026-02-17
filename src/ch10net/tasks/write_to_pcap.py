"""
Polls the DataPipe for Ethernet packets and writes them to a PCAP file using
Scapy's PcapWriter.
"""

from threading import Event

from scapy.all import PcapWriter

from tasks.data_pipe import DataPipe

__all__ = ['write_packets_to_pcap', 'deposit_ethernet_packets', 'terminate']

finish = Event()
terminate = Event()
_pipe = DataPipe(terminate)

def write_packets_to_pcap(outfile : str):
    global terminate, _pipe
    writer = PcapWriter(outfile, append=False)

    while not terminate.is_set():
        if (finish.is_set() and _pipe.is_empty()):
            break
        
        eth_packets = _pipe.retrieve()

        if writer:
            writer.write(eth_packets)

        writer.flush()

    writer.close()

def deposit_ethernet_packets(packets):
    global _pipe
    _pipe.deposit(packets)