
import pytest

from c10net.functions.progress_bar import ProgressBar

def test_progress_bar_initializes_with_bounds():
    pb = ProgressBar(24.0, 42.0)
    assert pb._start == pytest.approx(24.0)
    assert pb._end == pytest.approx(42.0)

def test_inverted_bounds_raises_value_error():
    with pytest.raises(ValueError):
        pb = ProgressBar(42, 24)

def test_can_set_bar_progress_relative():
    pb = ProgressBar(0.0, 100.0)
    pb.set_progress_relative(25.0)
    assert pb._progress == pytest.approx(25.0)

def test_can_set_bar_progress_absolute():
    pb = ProgressBar(0.0, 100.0)
    pb.set_progress_absolute(0.42)
    assert pb._progress == pytest.approx(42.0)

def test_clamp_relative():
    pb = ProgressBar(20, 40)

    value = 10.0
    value = pb._clamp(value)
    assert value == pytest.approx(20)

    value = 50.0
    value = pb._clamp(value)
    assert value == pytest.approx(40)

    value = 35.0
    value = pb._clamp(value)
    assert value == pytest.approx(35)

def test_clamp_absolute():
    pb = ProgressBar(0, 100)

    value = -0.5
    value = pb._clamp_abs(value)
    assert value == pytest.approx(0.0)

    value = 1.5
    value = pb._clamp_abs(value)
    assert value == pytest.approx(1.0)

    value = 0.76
    value = pb._clamp_abs(value)
    assert value == pytest.approx(0.76)

def test_progress_bar_output_format():
    pb = ProgressBar(0.0, 100.0)
    pb.set_progress_relative(50.0)
    bar = pb.get_bar()
    assert '===' in bar
    assert '---' in bar
    assert '%' in bar

def test_progress_bar_updates(capsys):
    pb = ProgressBar(0.0, 100.0)

    pb.set_progress_relative(0.0)
    bar = pb.get_bar()
    assert '0.0%' in bar

    pb.set_progress_relative(50.0)
    bar = pb.get_bar()
    assert '50.0%' in bar

    pb.set_progress_relative(100.0)
    bar = pb.get_bar()
    assert '100.0%' in bar