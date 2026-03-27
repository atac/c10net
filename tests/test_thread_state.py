
import pytest

from c10net.tasks.thread_state import ThreadState

def test_set_progress():
    ts = ThreadState()
    ts.set_progress(0.42)
    assert ts._progress == pytest.approx(0.42)

def test_get_progress():
    ts = ThreadState()
    ts.set_progress(0.56)
    assert ts.get_progress() == pytest.approx(0.56)

def test_set_progress_out_of_range_raises_value_error():
    with pytest.raises(ValueError):
        ts = ThreadState()
        ts.set_progress(3.0)
