
from threading import Thread

from c10net.tasks.task import Task

from c10net.tasks.parse_chapter10 import ParseChapter10
from c10net.tasks.chapter10_to_ethernet import Chapter10ToEthernet
from c10net.tasks.udp_replay import UdpReplay

class Replay(Task):
    def __init__(self, cli_args : dict):
        super().__init__(cli_args)

    
    def _init(self):
        print(self._cli_args)
        self._pulse_interval = 0.0
        if (
            not self._cli_args['pulse'] is None
            or not self._cli_args['pulse_interval'] is None
            ):
            self._pulse_interval = 1.0
            if (not self._cli_args['pulse_interval'] is None):
                self._pulse_interval = self._cli_args['pulse_interval']


    def _setup_linear(self):
        print(self._pulse_interval)
        replay = UdpReplay()
        convert = Chapter10ToEthernet(self._cli_args, direct_link=replay.direct_input())
        parse = ParseChapter10(
            self._cli_args['in_pathname'],
            self._cli_args['channel_ids'],
            self._cli_args['channel_types'],
            pulse_interval=self._pulse_interval,
            direct_link=convert.direct_input()
        )

        self._start_stage = parse
        self._stages.extend([parse, convert, replay])
        self._threads.append(Thread(target=self._start_stage.start))
        

    def _setup_parallel(self):
        parse = ParseChapter10(
            self._cli_args['in_pathname'],
            self._cli_args['channel_ids'],
            self._cli_args['channel_types'],
            pulse_interval=self._pulse_interval
        )
        convert = Chapter10ToEthernet(self._cli_args, source=parse.pipe_output())
        write = UdpReplay(source=convert.pipe_output())

        self._start_stage = parse
        self._stages.extend([parse, convert, write])
        self._threads.extend([
            Thread(target=parse.start),
            Thread(target=convert.start),
            Thread(target=write.start)
            ])