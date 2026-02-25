
from c10net.functions import transfer_header_generator as thg


def test_transfer_header_non_segmented_and_segmented():
    g = thg.UdpTransferHeaderGenerator()

    # Non-segmented
    headers = g.generate_transfer_headers(channel_id=1, packet_size=100)
    assert isinstance(headers, list)
    assert len(headers) == 1
    assert headers[0][0] == 0
    assert len(headers[0][1]) == 4

    # Segmented (force at least one segmentation)
    offsets = [0, g.MAX_MSG_SIZE]
    size = g.MAX_MSG_SIZE + 10
    headers = g.generate_transfer_headers(channel_id=2, packet_size=size)
    assert len(headers) >= 1
    # Segmented headers are 12 bytes (3 words)
    for index, (offset, header) in enumerate(headers):
        assert isinstance(offset, int)
        assert offset == offsets[index]
        assert len(header) == 12


def test_sequence_numbers_and_reset():
    g = thg.UdpTransferHeaderGenerator()
    # Channel sequence
    c1 = g.GetChannelSequenceNum(5)
    c2 = g.GetChannelSequenceNum(5)
    assert c2 == (c1 + 1) or (c1 == 0xFF and c2 == 0)

    # UDP sequence increments
    u1 = g.GetUdpSequenceNum()
    u2 = g.GetUdpSequenceNum()
    assert u2 == u1 + 1 or (u1 == 0xFFFFFF and u2 == 0)

    g.reset()
    assert g._seq_count == {}
    assert g._udp_sequence == 0x00
