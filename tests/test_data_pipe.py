
import pytest

from threading import Event

from c10net.stages.data_pipe import DataPipe, Empty, ShutDown


def test_deposit_and_retrieve():
    term = Event()
    dp = DataPipe(term, max_queue_size=10)

    dp.deposit([1, 2, 3])
    out = dp.retrieve()
    assert out == [1, 2, 3]

    out = dp.retrieve()
    assert len(out) == 0


def test_deposit_respects_terminate():
    term = Event()
    dp = DataPipe(term, max_queue_size=10)
    term.set()
    # deposit after terminate should not block or add items
    dp.deposit([4, 5])
    assert dp.retrieve() == []
