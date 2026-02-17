`python c10net.py -h`

    usage: c10net [-h] {convert_pcap,replay} ...

    Tools for network broadcast and replay of IRIG-106 Chapter 10/11 files.

    options:
    -h, --help            show this help message and exit

    commands:
    Choose a function to run

    {convert_pcap,replay}
                            Available commands

`python c10net.py replay -h`


    usage: c10net replay [-h] [--channels CHANNEL_IDS] [--types CHANNEL_TYPES] [--port PORT] [--ip IP] in_pathname

    Generate UDP packets from Chapter 10 file and send over a network interface

    options:
    -h, --help            show this help message and exit
    --port, -p PORT       The destination port number of the UDP packets
    --ip IP               The destination IP address of the UDP packets

    Chapter 10 Input File:
    in_pathname           Pathname of the Chapter 10 input file
    --channels, -c CHANNEL_IDS
                            List (comma-separated) of exclusive channel IDs to include in processing
    --types, -t CHANNEL_TYPES
                            List (comma-separated) of exclusive channel types to include in processing

`python c10net.py convert_pcap -h`

    usage: c10net convert_pcap [-h] [--channels CHANNEL_IDS] [--types CHANNEL_TYPES] [--out OUTFILE] in_pathname

    Convert Chapter 10 file to a PCAP file comprised of UDP packets

    options:
    -h, --help            show this help message and exit
    --out, -o OUTFILE     The output filepath of the converted PCAP file

    Chapter 10 Input File:
    in_pathname           Pathname of the Chapter 10 input file
    --channels, -c CHANNEL_IDS
                            List (comma-separated) of exclusive channel IDs to include in processing
    --types, -t CHANNEL_TYPES
                            List (comma-separated) of exclusive channel types to include in processing