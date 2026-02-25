
from c10net import c10net

def test_get_default_out_filepath():
    infile = 'C:\\data\\test.txt'
    outfile = 'C:\\data\\test.pcap'

    result = c10net._get_default_pcap_out_filepath_from_infile(infile)
    assert result == outfile