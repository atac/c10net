from datetime import *

from .transfer_header_generator import UdpTransferHeaderGenerator
from .udp_generator import UdpGenerator


class EthernetGenerator:
    def __init__(self, cli_args):
        self._initialize_udp_generator(cli_args)
        self._trans_header_gen = UdpTransferHeaderGenerator()

    def _initialize_udp_generator(self, args):
        port = 5006
        ip = "127.0.0.1"

        if hasattr(args, 'port'):
            port = args.port
        if hasattr(args, 'ip'):
            ip = args.ip
        
        self._udp_gen = UdpGenerator(destination_ip=ip, destination_port=port)

    def generate_from_chapter10(self, packet):
        udp_packets = []
        
        segs = self._with_transfer_headers(packet)
        for seg in segs:
            time = packet.get_time()
            time = time.replace(tzinfo=timezone.utc)
            udp = self._udp_gen.create_udp_packet(seg, time.timestamp())
            udp_packets.append(udp)

        return udp_packets

    def _with_transfer_headers(self, packet):
        data = packet.__bytes__()
        length = len(data)

        offset_header_pairs = self._trans_header_gen.generate_transfer_headers(packet.channel_id, length)

        segments = []

        for (offset, header) in offset_header_pairs:
            payload = data[offset:offset+self._trans_header_gen.MAX_MSG_SIZE]
            segments.append(header + payload)
            
        return segments