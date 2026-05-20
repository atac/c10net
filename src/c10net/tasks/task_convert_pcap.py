
from pathlib import Path
from threading import Thread

from c10net.tasks.task import Task

from c10net.stages.parse_chapter10 import ParseChapter10
from c10net.stages.chapter10_to_ethernet import Chapter10ToEthernet
from c10net.stages.write_to_pcap import WritePcap

class ConvertPcap(Task):
    def __init__(self, cli_args : dict):
        super().__init__(cli_args)


    def _init(self):
        if (self._cli_args['outfile'] is None
            or self._cli_args['outfile'] == ""):
            pathname = self._derive_outfile(self._cli_args['in_pathname'])
            self._cli_args['outfile'] = pathname


    def _setup_linear(self):
        write = WritePcap(self._cli_args['outfile'])
        convert = Chapter10ToEthernet(self._cli_args, direct_link=write.direct_input())
        parse = ParseChapter10(
            self._cli_args['in_pathname'],
            self._cli_args['channel_ids'],
            self._cli_args['channel_types'],
            direct_link=convert.direct_input()
        )

        self._start_stage = parse
        self._stages.extend([parse, convert, write])
        self._threads.append(Thread(target=self._start_stage.start))
        

    def _setup_parallel(self):
        parse = ParseChapter10(
            self._cli_args['in_pathname'],
            self._cli_args['channel_ids'],
            self._cli_args['channel_types']
        )
        convert = Chapter10ToEthernet(self._cli_args, source=parse.pipe_output())
        write = WritePcap(self._cli_args['outfile'], source=convert.pipe_output())

        self._start_stage = parse
        self._stages.extend([parse, convert, write])
        self._threads.extend([
            Thread(target=parse.start),
            Thread(target=convert.start),
            Thread(target=write.start)
            ])

        

    def _derive_outfile(self, in_pathname : str):
        inpath = Path(in_pathname)
        result = inpath.with_suffix('.pcap')
        return str(result)
    