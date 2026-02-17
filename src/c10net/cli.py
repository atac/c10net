from os.path import isfile
from argparse import *


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
    _add_commands(parser, infile_parser)
    
    return parser


def _add_commands(
        parser: ArgumentParser, 
        parent_parser: ArgumentParser
    ):
    
    subparser = parser.add_subparsers(
        title='commands',
        dest='command',
        description='Choose a function to run',
        help='Available commands')
    
    parser = subparser.add_parser(
        command_convert_pcap,
        description='Convert Chapter 10 file to a PCAP file comprised of UDP packets',
        parents=[parent_parser])
    
    _add_args_convert_pcap(parser)

    parser = subparser.add_parser(
        command_replay,
        description='Generate UDP packets from Chapter 10 file and send over a network interface',
        parents=[parent_parser])
    
    _add_args_replay(parser)


def _add_args_convert_pcap(parser : ArgumentParser):
    parser.add_argument(
        '--out',
        '-o',
        dest="outfile",
        help='The output filepath of the converted PCAP file')

def _add_args_replay(parser : ArgumentParser):
    parser.add_argument(
        '--port',
        '-p',
        dest='port',
        type=int,
        default=5006,
        help='The destination port number of the UDP packets')

    parser.add_argument(
        '--ip',
        dest='ip',
        type=str,
        help='The destination IP address of the UDP packets',
        default='127.0.0.1')


def _create_infile_parser():
    parser = ArgumentParser(
        'infile',
        add_help=False
    )

    group = parser.add_argument_group('Chapter 10 Input File')
    
    group.add_argument(
        'in_pathname',
        type=_file_path_name,
        help='Pathname of the Chapter 10 input file')
    
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
        raise ArgumentError('Specified input pathname is no a valid file')
    
    return s

def _channel_id_list(s : str):
    tokens = s.split(',')
    ids = [int(x) for x in tokens if len(x) != 0]

    if (any(n < 0 for n in ids)):
        raise ArgumentError('ChannelID must be positive integer')
    
    return ids

def _channel_type_list(s : str):
    tokens = s.split(',')
    return [int(x, 0) for x in tokens if len(x) != 0]