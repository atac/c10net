"""
UDP transfer header generator for ch10net.

Generates UDP transfer headers according to the IRIG-106 Chapter 10 standard
for both segmented and non-segmented transfers. This module is used in the 
process of converting Chapter 10 files to PCAP format or replaying them over 
a network interface.

State is maintained to ensure correct sequencing of segmented packets.
"""
import struct


#__all__ = ['generate_transfer_header', 'reset']

class UdpTransferHeaderGenerator():
    def __init__(self):
        self._seq_count = {}
        self._udp_sequence = 0x0
        self.MAX_BYTES_PER_MESSAGE = 32726
        self.MAX_MSG_SIZE = 1472

    def generate_transfer_headers(self, channel_id: int, packet_size: int):
        """
        Generate UDP transfer headers for a given channel ID.

        Returns a list of tuples containing (offset, header) for each segment.
        """
        headers = []

        length = packet_size

        if (length > self.MAX_MSG_SIZE):
            offset = 0
            seq_num = self.GetChannelSequenceNum(channel_id)

            while (length > 0):
                h = self.GetSegmentedUdpTransferHeader(channel_id, seq_num, offset)
                headers.append((offset, h))

                if (length > self.MAX_MSG_SIZE):
                    offset += self.MAX_MSG_SIZE
                    length -= self.MAX_MSG_SIZE
                else:
                    length = 0
        else:
            h = self.GetNonSegmentedUdpTransferHeader(channel_id)
            headers.append((0, h))

        return headers

    def reset(self):
        self._seq_count.clear()
        self._udp_sequence = 0x0

    def GetChannelSequenceNum(self, channel: int):
        num = self._seq_count.get(channel)

        if (num == None):
            num = 0
        else:
            if (num == 0xFF):
                num = 0
            else:
                num += 1

        self._seq_count[channel] = num

        return num

    def GetUdpSequenceNum(self):
        if (self._udp_sequence == 0xFFFFFF):
            self._udp_sequence = 0
        else:
            self._udp_sequence += 1
        
        return self._udp_sequence

    def GetUdpTransferHeaderFirstWord(self, channel: int, segmented: bool):
        ver = 0b0001
        type = 0b0001 if segmented else 0b0000
        seq_num = self.GetUdpSequenceNum()
        word = (seq_num << 8) | (type << 4) | ver
        header = struct.pack("<I", word)
        return header

    def GetNonSegmentedUdpTransferHeader(self, channel: int):
        return self.GetUdpTransferHeaderFirstWord(channel, False)

    def GetSegmentedUdpTransferHeader(self, channel: int, sequence_num: int, offset: int):
        headerWord1 = self.GetUdpTransferHeaderFirstWord(channel, True)

        word = (sequence_num << 16) | (channel & 0xFF)
        headerWord2 = struct.pack("<I", word)
        headerWord3 = struct.pack("<I", offset)

        return headerWord1 + headerWord2 + headerWord3