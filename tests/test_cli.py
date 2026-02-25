
import pytest
from argparse import ArgumentTypeError

from c10net import cli


def test_bad_command_fails():
    parser = cli.get_cli_parser()

    try:
        parser.parse_args(['not_a_command'])
        assert False
    except SystemExit:
        assert True

def test_convert_pcap_args(monkeypatch):
    monkeypatch.setattr(cli, "isfile", lambda x: True)

    parser = cli.get_cli_parser()

    try:
        parser.parse_args(['convert_pcap', '--out'])
        assert False
    except SystemExit:
        assert True
        
    try:
        pathname = 'converted.pcap'
        inname = 'input.txt'
        result = parser.parse_args(['convert_pcap', '--out=' + pathname, inname])
        assert result.outfile == pathname

        result = parser.parse_args(['convert_pcap', '-o ' + pathname, inname])
        assert result.outfile.strip() == pathname

        result = parser.parse_args(['convert_pcap', inname])
        assert not result.outfile

    except SystemExit:
        assert False

def test_replay_args(monkeypatch):
    monkeypatch.setattr(cli, "isfile", lambda x: True)

    infile = 'infile.txt'

    parser = cli.get_cli_parser()

    result = parser.parse_args(['replay', infile])
    assert not result.pulse
    assert not result.pulse_interval

    result = parser.parse_args(['replay', '--pulse', infile])
    assert result.pulse
    assert result.pulse == pytest.approx(1.0)
    assert not result.pulse_interval
    
    result = parser.parse_args(['replay', '--pulse-interval=3.5', infile])
    assert not result.pulse
    assert result.pulse_interval
    assert result.pulse_interval == pytest.approx(3.5)

    result = parser.parse_args(['replay', '--pulse', '--pulse-interval=3.5', infile])
    assert result.pulse
    assert result.pulse_interval
    assert result.pulse == pytest.approx(1.0)
    assert result.pulse_interval == pytest.approx(3.5)

def test_network_args():
    parser = cli._create_network_parser()

    result = parser.parse_args([])
    assert hasattr(result, 'port')
    assert hasattr(result, 'ip')

    result = parser.parse_args(['--port=12345'])
    assert result.port == 12345

    with pytest.raises(SystemExit):
        parser.parse_args(['--port=12a45'])

    result = parser.parse_args(['--ip=123.234.123.234'])
    assert result.ip == '123.234.123.234'

    with pytest.raises(SystemExit):
        parser.parse_args(['--ip=123.234.123.257'])

    
def test_infile_parser(monkeypatch):
    monkeypatch.setattr(cli, "isfile", lambda x: True)

    args = [
        'test.txt',
        '-c 1,2,3',
        '-t 1,0x2,3'
    ]
    parser = cli._create_infile_parser()

    result = parser.parse_args([args[0],])
    assert hasattr(result, 'in_pathname')
    assert len(getattr(result, 'channel_ids')) == 0
    assert len(getattr(result, 'channel_types')) == 0

    result = parser.parse_args([args[0], args[1]])
    assert hasattr(result, 'in_pathname')
    assert len(getattr(result, 'channel_ids')) == 3
    assert len(getattr(result, 'channel_types')) == 0

    result = parser.parse_args([args[0],args[2]])
    assert hasattr(result, 'in_pathname')
    assert len(getattr(result, 'channel_ids')) == 0
    assert len(getattr(result, 'channel_types')) == 3

    result = parser.parse_args(args)
    assert hasattr(result, 'in_pathname')
    assert len(getattr(result, 'channel_ids')) == 3
    assert len(getattr(result, 'channel_types')) == 3

def test_convert_channel_id_list():
    result = cli._channel_id_list("")
    assert len(result) == 0

    result = cli._channel_id_list("1")
    assert len(result) == 1

    result = cli._channel_id_list("1,2,3,")
    assert len(result) == 3
    
    with pytest.raises(ArgumentTypeError):
        cli._channel_id_list("1,2,a,4")
    
    with pytest.raises(ArgumentTypeError):
        cli._channel_id_list("1,-2,3")
    
    with pytest.raises(ArgumentTypeError):
        cli._channel_id_list("1,2.3,4")

def test_convert_channel_type_list():
    result = cli._channel_type_list("")
    assert len(result) == 0
    
    result = cli._channel_type_list("1")
    assert len(result) == 1
    
    result = cli._channel_type_list("0x5")
    assert len(result) == 1
    
    result = cli._channel_type_list("1,2,0x3,0xFF,4")
    assert len(result) == 5
    
    result = cli._channel_type_list("1,2,0X3,0XFF,4")
    assert len(result) == 5
    
    with pytest.raises(ArgumentTypeError):
        cli._channel_type_list("1,x3,4")

    with pytest.raises(ArgumentTypeError):
        cli._channel_type_list("1,string,3")
    
    with pytest.raises(ArgumentTypeError):
        cli._channel_type_list("1,-2,3")
    
    with pytest.raises(ArgumentTypeError):
        cli._channel_type_list("1,2.3,4")

def test_validate_ip_address():
    addr1 = '127.0.0.1'
    addr2 = '1.1.1.1'
    addr3 = '255.255.255.255'
    addr4 = '192.168.20.240'

    assert cli._ip_address(addr1) == addr1
    assert cli._ip_address(addr2) == addr2
    assert cli._ip_address(addr3) == addr3
    assert cli._ip_address(addr4) == addr4
    
    with pytest.raises(ArgumentTypeError):
        cli._ip_address('127.0.0.257')
    with pytest.raises(ArgumentTypeError):
        cli._ip_address('127.0.1')
    with pytest.raises(ArgumentTypeError):
        cli._ip_address('127..0.1')
    with pytest.raises(ArgumentTypeError):
        cli._ip_address('127.0.0.0.1')
    
def test_validate_port_number():
    port1 = 5006
    port2 = 12345
    port3 = 65536
    port4 = -1

    assert cli._port_number(port1) == port1
    assert cli._port_number(port2) == port2

    with pytest.raises(ArgumentTypeError):
        cli._port_number(port3)
    with pytest.raises(ArgumentTypeError):
        cli._port_number(port4)