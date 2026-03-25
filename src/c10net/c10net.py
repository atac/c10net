'''
Main entry for the c10net tools.

This module manages CLI arguments to coordinate module initialization.
'''

import sys
from threading import Thread, Event

from pytimedinput import timedKey

from . import cli
from . import chapter10_to_pcap
from . import chapter10_to_replay
# from .tasks import parse_chapter10 as parse_ch10
# from .tasks import chapter10_to_ethernet as ch10_to_eth
# from .tasks import write_to_pcap as write_to_pcap

from .tasks.worker import WorkerConfigError
from .tasks.task import Task
from .tasks.task_convert_pcap import ConvertPcap

_task = None # staging for Task object to be run

#_source_thread = None # Reference to the source thread to determine finished condition
#_threads = []  # List to keep track of threads for cleanup
#_terminate_events = []  # List to keep track of termination events for killing threads
#_finish_events = [] # List to keep track of finish events for clean shutdown of threads

should_terminate = Event()
should_finish = False


def cli_entry():
    args = cli.get_cli_parser().parse_args(sys.argv[1:])
    
    #print(args)

    if (args.command == cli.command_replay):
        stage_replay(args)
    elif (args.command == cli.command_convert_pcap):
        stage_convert_pcap(args)
    else:
        print("No command given. Use -h for help.")
        sys.exit(1)

    run()

    # global should_terminate
    # if (should_terminate.is_set()):
    #     terminate_all_threads()
        
    # for thread in _threads:
    #     thread.join()  # Wait for all threads to finish


def run():
    _task.start()
    wait_for_keypress_with_confirmation()

def wait_for_keypress_with_confirmation(prompt_key="Esc", confirm_prompt="Are you sure? (y/n): "):
    """Wait for a specific user keypress, then prompt for confirmation before returning."""
    global should_terminate

    print(f"Press {prompt_key} to exit...")

    while not should_terminate.is_set() and not finished():
        # Wait for the keypress
        key_pressed, key_timeout = timedKey(prompt_key, timeout=1)

        if (not key_timeout):
            # Prompt for confirmation
            response = input(confirm_prompt).strip().lower()
            if response in ('y', 'yes'):
                should_terminate.set()

def finished():
    """If source thread is done, set finish events. Returns True if finished."""
    global _source_thread, should_finish

    if (not should_finish and _source_thread and not _source_thread.is_alive()):
        should_finish = True
        for event in _finish_events:
            event.set()

    for thread in _threads:
        if thread.is_alive():
            return False

    return True

def terminate_all_threads():
    """Set all termination events to signal threads to exit."""
    for event in _terminate_events:
        event.set()



def stage_convert_pcap(cli_args):
    global _task

    try:
        _task = ConvertPcap(cli_args)
    except WorkerConfigError as err:
        err.add_note("Error in convert_pcap")
        raise err
    


def stage_replay(cli_args):
    None
    # TODO: implement
    #source_sink = (parse_ch10.retreive_packets, send_udp.deposit_packets)
    # _threads.append(Thread(target=parse_ch10.parse_file, args=(args)))
    # _threads.append(Thread(target=pipe_packets, args=source_sink))
    # _threads.append(Thread(target=send_udp.replay_packets, args=(args)))

    # _terminate_events.append(parse_ch10.terminate_event)
    # _terminate_events.append(send_udp.terminate_event)

    # _source_thread = _threads[0]
    #if (cli_args.parallel):
    if (False):
        None
    else:
        chapter10_to_replay.run_task(cli_args)
        sys.exit(0)


