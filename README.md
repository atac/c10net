# c10net

**Python utility to make Chapter 10/11 file packets available to network tools or replay as UDP packets.**

## Features

- Convert Chapter 10 data into a PCAP file containing UDP packets for analysis.
- Replay Chapter 10 data over the network, preserving original timing.
- Filter by channel ID and channel type during conversion or replay.
- Specify destination port and IP.

## Installation

Install from PyPI:

```bash
pip install c10net
```

Install optional dependencies:

- Test dependencies:
  ```bash
  pip install c10net[test]
  ```
- Development dependencies:
  ```bash
  pip install c10net[dev]
  ```

**Note:** `c10net` uses libpcap for pcap packet generation.  
On Windows, install [Npcap](https://nmap.org/npcap/) and ensure it is available to your system.

## Usage

The package installs a console script `c10net`. Run `c10net -h` for top-level help.

### `convert_pcap`

Convert Chapter 10 file to a PCAP file comprised of UDP packets.

```
c10net convert_pcap "C:\path\to\myfile.ch10"
```

With default options, a PCAP file is generated at "C:\path\to\myfile.pcap"

Use `ch10net convert_pcap -h` for more options.

### `replay`

Generate UDP packets from Chapter 10 file and send over a network interface.

```bash
c10net replay "C:\path\to\myfile.ch10"
```

With default options, UDP packets are replayed over available network interface with destination IP 127.0.0.1 and port 5006.

Use `ch10net replay -h` for more options.

### Network Options

* Use `--port` to set the destination port number of generated UDP packets.
* Use `--ip` to set the destination IP address of generated UDP packets.

#### Examples

Convert a Chapter 10 file to PCAP:

```bash
c10net convert_pcap input.ch10 --out output.pcap
```

Replay over the network (pulse setup packet every second):

```bash
c10net replay input.ch10 --pulse --ip 192.168.1.10 --port 49152
```

## Testing

Run the test suite with `pytest` (after installing the `test` optional dependency group):

```bash
pytest -q
```

## License

BSD-3-Clause
