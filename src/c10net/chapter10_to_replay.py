
import os

from chapter10 import C10, packet

import tasks.parse_chapter10 as pc10
import tasks.udp_replay as replay

import functions.ethernet_packet_generator as ethernet_gen
import functions.progress_bar as bar
import functions.setup_packet_pulse as pulse



def run_task(cli_args):
    eth_gen = ethernet_gen.EthernetGenerator(cli_args)

    pulser = None
    use_pulse = False
    if hasattr(cli_args, 'pulse_interval'):
        use_pulse = True
        pulse_interval = cli_args.pulse_interval
    
    pc10._set_filter_parameters(
        cli_args.channel_ids,
        cli_args.channel_types,
        use_pulse
    )

    have_time = False
    buf = []

    file_pos = 0.0
    size = os.path.getsize(cli_args.in_pathname)
    bar.set_bounds(0, size)

    file = C10(cli_args.in_pathname)

    for packet in file:
        file_pos += packet.packet_length
        bar.update_progress(file_pos)

        if use_pulse:
            if not pulser:
                if packet.channel_id == 0 and packet.data_type == 0x01:
                    pulser = pulse.SetupPacketPulse(packet)
                    pulser.set_interval(pulse_interval)
            else:
                setup_packet = pulser.get_pulse()
                if not setup_packet is None:
                    buf.append(setup_packet)

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
                    for eth in eth_packets:
                        replay.replay_packet_with_timestamp(eth)
            buf = []

        if (pc10._passes_filter(packet.channel_id, packet.data_type)):
            eth_packets = eth_gen.generate_from_chapter10(packet)
            for eth in eth_packets:
                replay.replay_packet_with_timestamp(eth)
            
    