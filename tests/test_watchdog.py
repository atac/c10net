import pytest
from threading import Event, Thread

from c10net.tasks.watchdog import Watchdog
from c10net.tasks.task import Task


def test_initializes_with_task(task_stub):
    ts = task_stub()
    wd = Watchdog(ts)
    assert wd._task is not None
    assert wd._task is ts

def test_starts_task(mocker, task_stub):
    ts = task_stub()
    mocked_start = mocker.patch.object(ts, "start")

    wd = Watchdog(ts)
    wd.start()

    mocked_start.assert_called_once()

def test_waits_to_join_until_work_is_done(task_stub):
    fake_work_done = Event()
    ts = task_stub(fake_work_done)
    wd = Watchdog(ts)

    thread = Thread(target=wd.start)
    thread.start()

    thread.join(0.1)
    assert thread.is_alive()

    fake_work_done.set()
    thread.join(1.0)

    assert not thread.is_alive()

def test_reports_progress(task_stub, capsys):
    fake_work_done = Event()
    ts = task_stub(fake_work_done)
    wd = Watchdog(ts)

    thread = Thread(target=wd.start)
    thread.start()
    thread.join(0.02)
    fake_work_done.set()
    thread.join()

    cap = capsys.readouterr()
    assert '42.1' in cap.out

def test_can_terminate_task(task_stub):
    fake_work_done = Event()
    ts = task_stub(fake_work_done)
    wd = Watchdog(ts)

    thread = Thread(target=wd.start)
    thread.start()
    wd.terminate()
    thread.join(0.1)

    # Must capture these and join the thread before making assertions,
    # otherwise the test will hang indefinitely on failure
    was_alive = thread.is_alive()
    work_was_done = fake_work_done.is_set()
    
    fake_work_done.set()
    thread.join()

    assert not was_alive
    assert not work_was_done

def test_can_finish_task(task_stub):
    fake_work_done = Event()
    ts = task_stub(fake_work_done)
    wd = Watchdog(ts)

    thread = Thread(target=wd.start)
    thread.start()
    wd.finish()
    thread.join(0.1)

    # Must capture these and join the thread before making assertions,
    # otherwise the test will hang indefinitely on failure
    was_alive = thread.is_alive()
    work_was_done = fake_work_done.is_set()
    
    fake_work_done.set()
    thread.join()

    assert not was_alive
    assert not work_was_done

def test_enters_run_loop(mocker, task_stub):
    wd = Watchdog(task_stub())
    mocked_run_loop = mocker.patch.object(wd, '_enter_run_loop')
    wd.start()
    
    mocked_run_loop.assert_called_once()


def test_prompts_user_for_termination(mocker, task_stub):
    fake_work_done = Event()
    ts = task_stub(fake_work_done)
    wd = Watchdog(ts)

    mocker.patch.object(wd, '_print_output', side_effect=KeyboardInterrupt)
    mocked_prompt = mocker.patch.object(wd, '_prompt_for_terminate')

    thread = Thread(target=wd.start)
    thread.start()
    thread.join(0.1)
    fake_work_done.set()
    thread.join()

    mocked_prompt.assert_called_once()
    

def test_respects_termination_request(mocker, task_stub):
    fake_work_done = Event()
    ts = task_stub(fake_work_done)
    wd = Watchdog(ts)
    mocker.patch.object(wd, '_print_output', side_effect=KeyboardInterrupt)
    mocker.patch.object(wd, "_prompt_for_terminate", return_value=True)

    thread = Thread(target=wd.start)
    thread.start()
    thread.join(0.1)
    was_alive = thread.is_alive()
    fake_work_done.set()
    thread.join()

    assert not was_alive

def test_resumes_on_termination_denial(mocker, task_stub):
    fake_work_done = Event()
    ts = task_stub(fake_work_done)
    wd = Watchdog(ts)
    mocker.patch.object(wd, '_print_output', side_effect=KeyboardInterrupt)
    mocker.patch.object(wd, "_prompt_for_terminate", return_value=False)

    thread = Thread(target=wd.start)
    thread.start()
    thread.join(0.1)
    was_alive = thread.is_alive()
    fake_work_done.set()
    thread.join()

    assert was_alive
