'''
Main entry for the ch10net tools.

This module manages CLI arguments to coordinate module initialization.
'''

import sys
from threading import Thread, Event

from pytimedinput import timedKey

import cli
import tasks.parse_chapter10 as parse_ch10
import tasks.chapter10_to_ethernet as ch10_to_eth
import tasks.write_to_pcap as write_to_pcap

import chapter10_to_pcap
import chapter10_to_replay

_source_thread = None # Reference to the source thread to determine finished condition
_threads = []  # List to keep track of threads for cleanup
_terminate_events = []  # List to keep track of termination events for killing threads
_finish_events = [] # List to keep track of finish events for clean shutdown of threads

should_terminate = Event()
should_finish = False


def main():
    args = cli.get_cli_parser().parse_args(sys.argv[1:])

    print(args)

    if (args.command == cli.command_replay):
        stage_replay(args)
    elif (args.command == cli.command_convert_pcap):
        stage_capture_pcap(args)
    else:
        print("No valid command provided. Use -h for help.")
        sys.exit(1)

    run()

    global should_terminate
    if (should_terminate.is_set()):
        terminate_all_threads()
        
    for thread in _threads:
        thread.join()  # Wait for all threads to finish


def run():
    global _threads

    for thread in _threads:
        thread.start()

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



def stage_capture_pcap(cli_args):
    if (cli_args.parallel): # TODO: test this process again
        _threads.append(Thread(
            target=parse_ch10.parse_file,
            args=(
                cli_args.channel_ids,
                cli_args.channel_types,
                cli_args.in_pathname,
                ch10_to_eth.deposit_chapter10_packets
            )))
        _threads.append(Thread(
            target=ch10_to_eth.build_ethernet_packets,
            args=(cli_args, write_to_pcap.deposit_ethernet_packets)
            ))
        _threads.append(Thread(
            target=write_to_pcap.write_packets_to_pcap,
            args=(cli_args.outfile,)
            ))

        _terminate_events.append(parse_ch10.terminate)
        _terminate_events.append(ch10_to_eth.terminate)
        _terminate_events.append(write_to_pcap.terminate)

        _finish_events.append(ch10_to_eth.finish)
        _finish_events.append(write_to_pcap.finish)

        global _source_thread
        _source_thread = _threads[0]
    else:
        chapter10_to_pcap.run_task(cli_args)
        sys.exit(0)
    


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
    if (cli_args.parallel):
        None
    else:
        chapter10_to_replay.run_task(cli_args)
        sys.exit(0)




if __name__ == "__main__":
    main()
