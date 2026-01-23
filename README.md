### TODO: This represents current functionality but changes should be made to allow more flexibility and function unification.

## Generate PCAP

Parses a Chapter 10 file, generates UDP transfer headers, and generates a PCAP file names output.pcap.

    python Ch10ToPCAP.py <infile>
        <infile>  :  Path to a Chapter 10 file


## Replay PCAP

Replays a .pcap file (hardcoded "Capture.pcap") on the Microsoft KM-TEST Loopback Adapter.

    python ReplayPCAP.py

