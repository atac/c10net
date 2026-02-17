from scapy.all import *
import time

_first_real_time = None
_first_file_time = None

def replay_packet_with_timestamp(ethernet_packet):
    global _first_real_time, _first_file_time
    
    # Calculate the time delay from the previous packet's timestamp to the current packet's timestamp
    if not _first_real_time or not _first_file_time:
        _first_real_time = time.time()
        _first_file_time = ethernet_packet.time

    real_offset = time.time() - _first_real_time
    file_offset = ethernet_packet.time - _first_file_time

    delay = file_offset - real_offset

    if (delay >= 0.0):
        # Wait for the calculated delay (relative to the previous packet)
        time.sleep(float(delay))

    # Send the packet over the network
    send(ethernet_packet.payload, verbose=False)
