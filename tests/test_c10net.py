
import pytest
from threading import Event

from c10net import c10net
from c10net.tasks.worker import WorkerConfigError
from c10net.tasks.task_convert_pcap import ConvertPcap

def test_stage_convert_pcap_throws_config_error():
    with pytest.raises(WorkerConfigError):
        c10net.stage_convert_pcap({})

    assert c10net._task is None

def test_stage_convert_pcap_initializes_task(mocker):
    mocker.patch('c10net.tasks.task_convert_pcap.ConvertPcap._setup_linear')
    c10net.stage_convert_pcap({'in_pathname' : 'C:/data/test.ch10', 'parallel':False, 'outfile' : None})
    assert c10net._task is not None
    assert isinstance(c10net._task, ConvertPcap)

def test_run_starts_watchdog(mocker, task_stub):
    mocked_start = mocker.patch('c10net.watchdog.Watchdog.start')
    c10net._task = task_stub()
    c10net.run()
    mocked_start.assert_called_once()

