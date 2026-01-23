from scapy.all import *
import time

first_time = 0.0
last_time = 0.0
progress = 0



def replay_pcap_with_timestamps(pcap_file, interface="Microsoft KM-TEST Loopback Adapter"):
    """
    Replays packets from a pcap file over the specified network interface while preserving the
    original timestamps of the packets.
    
    :param pcap_file: Path to the pcap file.
    :param interface: The network interface to send packets over.
    """
    global first_time
    global last_time

    print("Reading PCAP file...")

    # Read the pcap file
    reader = PcapReader(pcap_file)
    packets = reader.read_all()
    #packets = rdpcap(pcap_file)

    first_time = packets[0].time
    last_time = packets[len(packets) - 1].time
    
    # Get the timestamp of the first packet
    previous_packet_time = packets[0].time

    delay = 0.0
    
    print("Starting replay...")
    
    # Loop through each packet
    for packet in packets:
        update_progress(packet.time)

        # Calculate the time delay from the previous packet's timestamp to the current packet's timestamp
        delay = packet.time - previous_packet_time
        previous_packet_time = packet.time

        # Wait for the calculated delay (relative to the previous packet)
        time.sleep(float(delay))

        # modify destination port and IP
        packet.payload.dst = '169.254.210.10'
        packet.payload.payload.dport = 5006
        
        # Send the packet over the network
        sendp(packet, iface=interface, verbose=False)
        #print(f"Replayed packet: {packet.summary()} at {delay:.2f} seconds")
        
    print("Replay complete.")

    

def update_progress(timestamp: float):
    global progress

    time_range = last_time - first_time
    curr = timestamp - first_time

    percent = (curr / time_range) * 100.0

    if (int(percent > progress)):
        progress = int(percent)
        print_progress()
    
def print_progress():
    progress_bar = generate_progress_bar()
    print('\r' + progress_bar, end='')

def generate_progress_bar():
    bar = '|'

    bar_size = 50

    fraction = int((progress / 100.0) * bar_size)

    for i in range(0, fraction):
        bar += '='
    
    for i in range(0, bar_size-fraction):
        bar += '-'

    bar += f'| {progress}%   '

    return bar



if __name__ == "__main__":
    # Path to your pcap filec
    pcap_file = "Capture.pcap"  # Change this to your actual file path
    
    # Replay the pcap file over localhost with timestamps
    replay_pcap_with_timestamps(pcap_file)
