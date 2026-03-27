
import pytest

from c10net.tasks.worker import WorkerConfigError
from c10net.tasks.task_convert_pcap import ConvertPcap

def test_invalid_config_raises_exception():
    with pytest.raises(WorkerConfigError):
        ConvertPcap({}).start()
    
def test_parallel_option_calls_setup_parallel(mocker):
    mocked_parallel = mocker.patch(
        'c10net.tasks.task_convert_pcap.ConvertPcap._setup_parallel')
    cp = ConvertPcap({"parallel":True, "in_pathname":"test"})

    mocked_parallel.assert_called_once()
    
def test_not_parallel_option_calls_setup_linear(mocker):
    mocked_linear = mocker.patch(
        'c10net.tasks.task_convert_pcap.ConvertPcap._setup_linear')
    cp = ConvertPcap({"parallel":False, "in_pathname":"test"})

    mocked_linear.assert_called_once()

def test_call_derive_outfile(mocker):
    classpath = 'c10net.tasks.task_convert_pcap.ConvertPcap.'
    mocker.patch(classpath + '_setup_linear')
    mocked_derive_outfile = mocker.patch(classpath + '_derive_outfile')
    
    cp  = ConvertPcap({"parallel":False, "in_pathname" : "C:\data\myfile.ch10"})

    mocked_derive_outfile.assert_called_once()

def test_derives_default_out_pathname_when_none_provided(mocker):
    mocked_parallel = mocker.patch(
        'c10net.tasks.task_convert_pcap.ConvertPcap._setup_linear')
    
    infile = 'C:\\data\\test.ch10'
    outfile = 'C:\\data\\test.pcap'
    
    cp  = ConvertPcap({"parallel":False, "in_pathname" : infile})

    assert cp._cli_args['outfile'] == outfile