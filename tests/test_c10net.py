import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "c10net"))
sys.path.insert(0, str(ROOT / "src"))

import c10net.c10net as c10net

def test_get_default_out_filepath():
    infile = 'C:\\data\\test.txt'
    outfile = 'C:\\data\\test.pcap'

    result = c10net._get_default_pcap_out_filepath_from_infile(infile)
    assert result == outfile