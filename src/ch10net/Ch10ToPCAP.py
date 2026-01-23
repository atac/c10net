from GeneratePCAP import PcapGenerator
from chapter10 import C10
import sys
import struct

MAX_BYTES_PER_MESSAGE = 32726
MAX_MSG_SIZE = 1472

data_types = {0x40, 0x41, 0x42, 0x43, 0x44}
channels = {10}

seq_count = {}
udp_sequence = 0x0

def GetChannelSequenceNum(channel: int):
    num = seq_count.get(channel)

    if (num == None):
        num = 0
    else:
        if (num == 0xFF):
            num = 0
        else:
            num += 1

    seq_count[channel] = num

    return num

def GetUdpSequenceNum():
    global udp_sequence
    if (udp_sequence == 0xFFFFFF):
        udp_sequence = 0
    else:
        udp_sequence += 1
    
    return udp_sequence

def GetUdpTransferHeaderFirstWord(channel: int, segmented: bool):
    ver = 0b0001
    type = 0b0001 if segmented else 0b0000
    seq_num = GetUdpSequenceNum()
    word = (seq_num << 8) | (type << 4) | ver
    header = struct.pack("!I", word)
    return header

def GetNonSegmentedUdpTransferHeader(channel: int):
    return GetUdpTransferHeaderFirstWord(channel, False)

def GetSegmentedUdpTransferHeader(channel: int, sequence_num: int, offset: int):
    headerWord1 = GetUdpTransferHeaderFirstWord(channel, True)

    word = (sequence_num << 16) | (channel & 0xFF)
    headerWord2 = struct.pack("!I", word)
    headerWord3 = struct.pack("!I", offset)

    return headerWord1 + headerWord2 + headerWord3

def CreatePacket(payload: bytes, timestamp: float):
        capture.create_udp_packet(payload, time.timestamp())


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Invalid number of arguments")
        exit()

    infile = sys.argv[1]

    capture = PcapGenerator("output.pcap")

    counter = 0
    iterations = 0

    for packet in C10(infile):
        if packet.data_type not in data_types:
            continue
        if packet.channel_id not in channels:
            continue

        time = packet.get_time()
        data = packet.__bytes__()
        length = len(data)

        if (length > MAX_MSG_SIZE):
            offset = 0
            seq_num = GetChannelSequenceNum(packet.channel_id)
            while (True):
                payload = GetSegmentedUdpTransferHeader(packet.channel_id, seq_num, offset)
                if (length > MAX_MSG_SIZE):
                    payload += data[offset:offset+MAX_MSG_SIZE]
                    offset += MAX_MSG_SIZE
                    length -= MAX_MSG_SIZE
                    CreatePacket(payload, time.timestamp())
                else:
                    payload += data[offset:]
                    CreatePacket(payload, time.timestamp())
                    break
        else:
            transferHeader = GetNonSegmentedUdpTransferHeader(packet.channel_id)
            payload = transferHeader + data
            CreatePacket(payload, time.timestamp())

        counter += 1

        if (counter >= 1000):
            counter = 0
            capture.save_to_pcap()
            iterations += 1
        
        #if (iterations == 3):
        #    exit()
    
    capture.save_to_pcap()
    capture.close()