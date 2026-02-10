"""
UDP transfer header generator for ch10net.

Generates UDP transfer headers according to the IRIG-106 Chapter 10 standard
for both segmented and non-segmented transfers. This module is used in the 
process of converting Chapter 10 files to PCAP format or replaying them over 
a network interface.

State is maintained to ensure correct sequencing of segmented packets.
"""
import struct


__all__ = ['generate_transfer_header', 'reset']

_seq_count = {}
_udp_sequence = 0x0

MAX_BYTES_PER_MESSAGE = 32726
MAX_MSG_SIZE = 1472

def generate_transfer_headers(channel_id: int, packet_size: int):
    """
    Generate UDP transfer headers for a given channel ID.

    Returns a list of tuples containing (offset, header) for each segment.
    """
    headers = []

    if (length > MAX_MSG_SIZE):
        offset = 0
        seq_num = GetChannelSequenceNum(channel_id)

        while (length > 0):
            h = GetSegmentedUdpTransferHeader(channel_id, seq_num, offset)
            headers.append((offset, h))

            if (length > MAX_MSG_SIZE):
                offset += MAX_MSG_SIZE
                length -= MAX_MSG_SIZE
            else:
                length = 0
    else:
        h = GetNonSegmentedUdpTransferHeader(channel_id)
        headers.append((0, h))

    return headers

def reset():
    _seq_count.clear()
    global _udp_sequence
    _udp_sequence = 0x0

def GetChannelSequenceNum(channel: int):
    num = _seq_count.get(channel)

    if (num == None):
        num = 0
    else:
        if (num == 0xFF):
            num = 0
        else:
            num += 1

    _seq_count[channel] = num

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
    header = struct.pack("<I", word)
    return header

def GetNonSegmentedUdpTransferHeader(channel: int):
    return GetUdpTransferHeaderFirstWord(channel, False)

def GetSegmentedUdpTransferHeader(channel: int, sequence_num: int, offset: int):
    headerWord1 = GetUdpTransferHeaderFirstWord(channel, True)

    word = (sequence_num << 16) | (channel & 0xFF)
    headerWord2 = struct.pack("<I", word)
    headerWord3 = struct.pack("<I", offset)

    return headerWord1 + headerWord2 + headerWord3