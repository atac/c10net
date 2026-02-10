from scapy.all import Ether, IP, UDP, Raw
from typing import List

__all__ = ['set_udp_properties', 'create_udp_packet']

src_ip = ""
dst_ip = ""
src_port = 0
dst_port = 0
src_mac = ""
dst_mac = ""

def set_udp_properties( 
        source_ip="192.168.0.1", 
        destination_ip="127.0.0.1",
        source_port=12345, 
        destination_port=5006, 
        source_mac="00:11:22:33:44:55",
        destination_mac="ff:ff:ff:ff:ff:ff"
        ):
    global src_ip, dst_ip, src_port, dst_port, src_mac, dst_mac
    src_ip = source_ip
    dst_ip = destination_ip
    src_port = source_port
    dst_port = destination_port
    src_mac = source_mac
    dst_mac = destination_mac

def create_udp_packet(payload: bytes, timestamp_s: float):
    
    ether = Ether(src=src_mac, dst=dst_mac)
    ip = IP(src=src_ip, dst=dst_ip)
    udp = UDP(sport=src_port, dport=dst_port)
    packet = ether / ip / udp / Raw(load=payload)
    packet.time = timestamp_s

    return packet