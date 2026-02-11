from scapy.all import Ether, IP, UDP, Raw

class UdpGenerator:
    def __init__(
            self,
            source_ip="192.168.0.1", 
            destination_ip="127.0.0.1",
            source_port=12345, 
            destination_port=5006, 
            source_mac="00:11:22:33:44:55",
            destination_mac="ff:ff:ff:ff:ff:ff"
            ):
        self._src_ip = source_ip
        self._dst_ip = destination_ip
        self._src_port = source_port
        self._dst_port = destination_port
        self._src_mac = source_mac
        self._dst_mac = destination_mac

    def create_udp_packet(self, payload: bytes, timestamp_s: float):
        
        ether = Ether(src=self._src_mac, dst=self._dst_mac)
        ip = IP(src=self._src_ip, dst=self._dst_ip)
        udp = UDP(sport=self._src_port, dport=self._dst_port)
        packet = ether / ip / udp / Raw(load=payload)
        packet.time = timestamp_s

        return packet