
import os

from chapter10 import C10

import tasks.parse_chapter10 as pc10
import tasks.write_to_pcap as w2pcap

import functions.ethernet_packet_generator as ethernet_gen
import functions.progress_bar as bar


def run_task(cli_args):
    eth_gen = ethernet_gen.EthernetGenerator(cli_args)
    pcap = w2pcap.PcapWriter(cli_args.outfile, append=False)

    pc10._set_filter_parameters(
        cli_args.channel_ids,
        cli_args.channel_types
    )

    file_pos = 0.0
    size = os.path.getsize(cli_args.in_pathname)
    bar.set_bounds(0, size)

    have_time = False
    buf = []

    for packet in C10(cli_args.in_pathname):
        file_pos += packet.packet_length
        bar.update_progress(file_pos)

        if (not have_time):
            if (packet.parent and packet.parent.last_time is not None):
                have_time = True
            else:
                buf.append(packet)
                continue

        if (len(buf) > 0):
            for p in buf:
                p.parent.last_time = packet.parent.last_time
                if (pc10._passes_filter(p.channel_id, p.data_type)):
                    eth_packets = eth_gen.generate_from_chapter10(p)
                    pcap.write(eth_packets)
            buf = []

        if (pc10._passes_filter(packet.channel_id, packet.data_type)):
            eth_packets = eth_gen.generate_from_chapter10(packet)
            pcap.write(eth_packets)
    
    pcap.flush()
    pcap.close()