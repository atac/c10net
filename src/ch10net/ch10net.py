'''
Main entry for the ch10net tools.

This module manages CLI arguments to coordinate module initialization.
'''

import sys


from cli import *


def main():
    parser = get_cli_parser()
    
    args = parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    main()