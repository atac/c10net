# ch10net Software Requirements

### Chapter 10 Files

* Open Chapter 10 files
* Choose input pathname
* Extract packets from Chapter 10 files
* Parse Chapter 10 headers
* Choose to filter packets by Channel ID
* Choose to filter packets by Channel Data Type

### UDP Transfer Headers

* Generate Format 1 UDP Transfer Headers for non-segmented data
* Track UDP Message Sequence Number
* Generate Format 1 UDP Transfer Headers for segmented data
* Segment Chapter 10 packets
* Track Channel Sequence Number by Channel ID
* Track Segment Offset for segmented packet data
* Combine UDP Transfer Headers with packet data

### UDP Packets

* Generate UDP datagram with a Chapter 10 Transfer payload
* Choose UDP Datagram destination IP address
* Choose UDP Datagram destination port number
* Modify UDP destination IP address
* Modify UDP destination port number

### Networking

* Discover available network interfaces
* Select a network interface
* Send UDP Datagram on selected network interface

### Storage

* Choose output to PCAP
* Generate PCAP packets from UDP datagrams
* Choose output pathname
* Output to PCAP file

### Replay

* Choose input PCAP pathname
* Open PCAP file
* Retrieve UDP Datagrams from PCAP file

### Timing

* Choose input-lead timing
* Choose user-defined constant timing
* Trigger timed actions based on timing input

