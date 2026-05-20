'''
Main entry for the c10net tools.

This module manages CLI arguments to coordinate module initialization.
'''

import sys

# from pytimedinput import timedKey

from . import cli

from .tasks.worker import WorkerConfigError
from .tasks.task_convert_pcap import ConvertPcap
from .tasks.task_replay import Replay
from .tasks.watchdog import Watchdog

_task = None # staging for Task object to be run

def cli_entry():
    args = cli.get_cli_parser().parse_args(sys.argv[1:])
    
    #print(args)

    if (args.command == cli.command_replay):
        stage_replay(vars(args))
    elif (args.command == cli.command_convert_pcap):
        stage_convert_pcap(vars(args))
    else:
        print("No command given. Use -h for help.")
        sys.exit(1)

    run()

def run():
    global _task

    wd = Watchdog(_task)
    wd.start()


def stage_convert_pcap(cli_args):
    global _task

    try:
        _task = ConvertPcap(cli_args)
    except WorkerConfigError as err:
        err.add_note("Error in convert_pcap")
        raise err


def stage_replay(cli_args):
    global _task

    try:
        _task = Replay(cli_args)
    except WorkerConfigError as err:
        err.add_note("Error in convert_pcap")
        raise err
