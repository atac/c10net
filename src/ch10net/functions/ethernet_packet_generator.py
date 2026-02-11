from ch10net.functions.transfer_header_generator import UdpTransferHeaderGenerator
from ch10net.functions.udp_generator import UdpGenerator


class EthernetGenerator:
    def __init__(self, cli_args):
        self._initialize_udp_generator(cli_args)
        self._trans_header_gen = UdpTransferHeaderGenerator()

    def _initialize_udp_generator(self, args):
        port = 5006
        ip = "127.0.0.1"

        if (args.port):
            port = args.port
        if (args.ip):
            ip = args.ip
        
        self._udp_gen = UdpGenerator(destination_ip=ip, destination_port=port)

    def generate_from_chapter10(self, packets):
        udp_packets = []
        
        for packet in packets:
            segs = self._with_transfer_headers(packet)
            for seg in segs:
                udp = self._udp_gen.create_udp_packet(seg, packet.get_time())
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