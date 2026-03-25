from threading import Thread
from pathlib import Path

from c10net.tasks.task import Task
from c10net.tasks.worker import WorkerConfigError
import c10net.chapter10_to_pcap as c2pcap

from c10net.tasks.parse_chapter10 import ParseChapter10
from c10net.tasks.chapter10_to_ethernet import C10ToEthernet
from c10net.tasks.write_to_pcap import WritePcap

# from c10net.tasks import parse_chapter10 as parse_ch10
# from c10net.tasks import chapter10_to_ethernet as ch10_to_eth
# from c10net.tasks import write_to_pcap as write_to_pcap

class ConvertPcap(Task):
    def __init__(self, cli_args : dict):
        super().__init__(cli_args)

        self._init()

        if self._cli_args.parallel:
            self._setup_parallel()
        else:
            self._setup_linear()


    def start(self):
        if self._task_func is None:
            raise WorkerConfigError("Worker not configured")
        self._task_func()

    def _init(self):
        if not self._cli_args.outfile:
            pn = self._derive_out_pathname(self._cli_args.in_pathname)
            self._cli_args.outfile = pn

    def _setup_linear(self):
        write = WritePcap(self._cli_args.outfile)
        convert = C10ToEthernet(self._cli_args, write.direct_input())
        parse = ParseChapter10(
            self._cli_args.in_pathname,
            self._cli_args.channel_ids,
            self._cli_args.channel_types,
            sink=convert.direct_input()
        )

        self._task_func = parse.start
        self._stages.extend([parse, convert, write])

    def _setup_parallel(self):
        pass
        # TODO: instantiate stages with the correct sinks
        # TODO: 
        # self._subtasks.append()


        # super().state.threads.append(Thread(
        #     target=parse_ch10.parse_file,
        #     args=(
        #         self.cli_args.channel_ids,
        #         self.cli_args.channel_types,
        #         self.cli_args.in_pathname,
        #         ch10_to_eth.deposit_chapter10_packets
        #     )))
        # super().state.threads.append(Thread(
        #     target=ch10_to_eth.build_ethernet_packets,
        #     args=(self.cli_args, write_to_pcap.deposit_ethernet_packets)
        #     ))
        # super().state.threads.append(Thread(
        #     target=write_to_pcap.write_packets_to_pcap,
        #     args=(self.cli_args.outfile,)
        #     ))

        # _terminate_events.append(parse_ch10.terminate)
        # _terminate_events.append(ch10_to_eth.terminate)
        # _terminate_events.append(write_to_pcap.terminate)

        # _finish_events.append(ch10_to_eth.finish)
        # _finish_events.append(write_to_pcap.finish)

        # global _source_thread
        # _source_thread = _threads[0]

        

    def _derive_out_pathname(self, in_pathname : str):
        inpath = Path(in_pathname)
        result = inpath.with_suffix('.pcap')
        return str(result)