'''
Main entry for the ch10net tools.

This module manages CLI arguments to coordinate module initialization.
'''

import sys
from threading import Thread, Event

from pytimedinput import timedKey
from cli import *
import parse_chapter10 as parse_ch10

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
    source_sink = (parse_ch10.retreive_packets, send_udp.deposit_packets)
    _threads.append(Thread(target=parse_ch10.parse_file, args=(args)))
    _threads.append(Thread(target=pipe_packets, args=source_sink))
    _threads.append(Thread(target=send_udp.replay_packets, args=(args)))

    _terminate_events.append(parse_ch10.terminate_event)
    _terminate_events.append(send_udp.terminate_event)


def stage_capture_pcap(args):
    source_sink = (parse_ch10.retreive_packets, gen_pcap.deposit_packets)
    _threads.append(Thread(target=parse_ch10.parse_file, args=(args)))
    _threads.append(Thread(target=pipe_packets, args=source_sink))
    _threads.append(Thread(target=gen_pcap.capture_pcap_packets, args=(args)))

    _terminate_events.append(parse_ch10.terminate_event)
    _terminate_events.append(gen_pcap.terminate_event)


def pipe_packets(source_func, sink_func):
    """Continuously pipe packets from a source function to a sink function until termination is requested."""
    while not should_exit.is_set():
        packets = source_func()
        sink_func(packets)

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
