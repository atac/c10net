'''
Main entry for the ch10net tools.

This module manages CLI arguments to coordinate module initialization.
'''

import sys
from threading import Thread, Event
from ch10net.parse_chapter10 import *

from pytimedinput import timedKey
from cli import *

_threads = []  # List to keep track of threads for cleanup
_terminate_events = []  # List to keep track of termination events for cleanup

should_exit = Event()


def main():
    args = get_cli_parser().parse_args(sys.argv[1:])

    if (args.command == command_replay):
        stage_replay(args)
    elif (args.command == command_convert_pcap):
        stage_capture_pcap(args)

    run()
    cleanup()


def stage_replay(args):
    _threads.append(Thread(target=parse_file, args=(args)))
    _threads.append(Thread(target=replay_packets, args=(args)))


def stage_capture_pcap(args):
    _threads.append(Thread(target=parse_file, args=(args)))
    _threads.append(Thread(target=capture_pcap_packets, args=(args)))


def run():
    for thread in _threads:
        thread.start()

    wait_for_keypress_with_confirmation()
    

def wait_for_keypress_with_confirmation(prompt_key="Esc", confirm_prompt="Are you sure? (y/n): "):
    """Wait for a specific user keypress, then prompt for confirmation before returning."""

    print(f"Press {prompt_key} to exit...")
    
    while not should_exit.is_set():
        # Wait for the keypress
        key_pressed, key_timeout = timedKey(prompt_key, timeout=1)
        
        if (not key_timeout):
            # Prompt for confirmation
            response = input(confirm_prompt).strip().lower()
            if response in ('y', 'yes'):
                should_exit.set()


def cleanup():
    """Perform any necessary cleanup before exiting."""
    for event in _terminate_events:
        event.set()  # Signal all threads to terminate

    for thread in _threads:
        thread.join()  # Wait for all threads to finish

if __name__ == "__main__":
    main()
