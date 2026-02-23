from os.path import isfile
from argparse import *
import ipaddress


command_replay = 'replay'
command_convert_pcap = 'convert_pcap'

__all__ = ['get_cli_parser', 'command_replay', 'command_convert_pcap']

def get_cli_parser():
    '''Creates and returns the argparse object according to the CLI requirements.'''

    parser = ArgumentParser(
        prog = 'c10net',
        description='Tools for network broadcast and replay of IRIG-106 Chapter 10/11 files.')

    # parser.add_argument(
    #     '--parallel',
    #     action='store_true',
    #     help='Whether to run the processing stages in parallel threads [when available]'
    # )

    infile_parser = _create_infile_parser()
    network_parser = _create_network_parser()
    _add_commands(parser, infile_parser, network_parser)
    
    return parser


def _add_commands(
        parser: ArgumentParser, 
        infile_parser: ArgumentParser,
        network_parser: ArgumentParser
    ):
    
    subparser = parser.add_subparsers(
        title='commands',
        dest='command',
        description='Choose a function to run. Use with -h for more details',
        help='Available commands')
    
    parser = subparser.add_parser(
        command_convert_pcap,
        description='Convert Chapter 10 file to a PCAP file comprised of UDP packets',
        parents=[infile_parser, network_parser])
    
    _add_args_convert_pcap(parser)

    parser = subparser.add_parser(
        command_replay,
        description='Generate UDP packets from Chapter 10 file and send over a network interface',
        parents=[infile_parser, network_parser])
    
    _add_args_replay(parser)


def _add_args_convert_pcap(parser : ArgumentParser):
    parser.add_argument(
        '--out',
        '-o',
        dest="outfile",
        help='The output filepath of the converted PCAP file')

def _add_args_replay(parser : ArgumentParser):
    parser.add_argument(
        '--pulse',
        const=1.0,
        action='store_const',
        help='Pulse the setup packet at the default interval of 1 second'
    )
    parser.add_argument(
        '--pulse-interval',
        dest='pulse_interval',
        type=float,
        help='Pulse the setup packet at the specified interval in seconds'
    )

def _create_network_parser():
    parser = ArgumentParser(
        'network',
        add_help=False
    )

    group = parser.add_argument_group('Network and packet settings')

    group.add_argument(
        '--port',
        '-p',
        dest='port',
        type=_port_number,
        default=5006,
        help='The destination port number of generated UDP packets (default=5006)')

    group.add_argument(
        '--ip',
        dest='ip',
        type=_ip_address,
        help='The destination IP address of generated UDP packets (default=127.0.0.1)',
        default='127.0.0.1')
    
    return parser

def _create_infile_parser():
    parser = ArgumentParser(
        'infile',
        add_help=False
    )

    group = parser.add_argument_group('Chapter 10 Input File')
    
    group.add_argument(
        'in_pathname',
        type=_file_path_name,
        help='(REQUIRED) Pathname of the Chapter 10 input file')
    
    group.add_argument(
        '--channels',
        '-c',
        dest='channel_ids',
        type=_channel_id_list,
        default=[],
        help='List (comma-separated) of exclusive channel IDs to include in processing')
    
    group.add_argument(
        '--types',
        '-t',
        dest='channel_types',
        type=_channel_type_list,
        default=[],
        help='List (comma-separated) of exclusive channel types to include in processing')
    
    return parser

def _file_path_name(s : str):
    if (not isfile(s)):
        raise FileExistsError('Specified input pathname is not a valid file')
    
    return s

def _channel_id_list(s : str):
    tokens = s.split(',')
    try:
        ids = [int(x) for x in tokens if len(x) != 0]
        if (any(n < 0 for n in ids)):
            raise ValueError('Provided value is negative')

    except ValueError as err:
        raise ArgumentTypeError((
            'ChannelID must be positive integer', 
            *err.args
            ))

    return ids

def _channel_type_list(s : str):
    tokens = s.split(',')
    try:
        types = [int(x, 0) for x in tokens if len(x) != 0]
        if (any(n < 0 for n in types)):
            raise ValueError('Provided value is negative')
        
    except ValueError as err:
        raise ArgumentTypeError((
            'Channel type must be positive integer (allows hex in the form 0xFF)', 
            *err.args
            ))


    return types

def _ip_address(addr : str):
    try:
        ipaddress.ip_address(addr)
        return addr
    except ValueError as err:
        raise ArgumentTypeError(('Invalid IP address', *err.args))
    
def _port_number(port_str : str):
    try:
        port_int = int(port_str)
        if 0 <= port_int <= 65535:
            return port_int
        else:
            raise ArgumentTypeError(('Port number not in the valid range',))
    except ValueError as err:
        raise ArgumentTypeError(('Invalid port number', *err.args))