from scapy.all import Ether, IP, UDP, Raw, PcapWriter
from typing import List

class PcapGenerator:
    def __init__(self, filename="output.pcap"):
        self.writer = PcapWriter(filename, append=False)
        self.filename = filename
        self.packets: List = []

    def create_udp_packet(self, payload: bytes, timestamp_s: float, src_ip="192.168.0.1", dst_ip="169.254.210.10",
                          src_port=12345, dst_port=5006, iface_mac="00:11:22:33:44:55"):
        
        ether = Ether(src=iface_mac, dst="ff:ff:ff:ff:ff:ff")
        ip = IP(src=src_ip, dst=dst_ip)
        udp = UDP(sport=src_port, dport=dst_port)
        packet = ether / ip / udp / Raw(load=payload)
        packet.time = timestamp_s

        # Store packet in list
        self.packets.append(packet)
        #print("Packet created and stored.")

    def save_to_pcap(self):
        if self.packets:
            for packet in self.packets:
                self.writer.write(packet)

            #wrpcap(self.filename, self.packets, append=False)

            msg = f'{len(self.packets)} packet(s) written to {self.filename}'
            print(msg)

            self.writer.flush()

            self.packets.clear()
        else:
            print("No packets to write.")

    def close(self):
        self.writer.close()