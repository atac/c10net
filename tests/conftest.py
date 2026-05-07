import pytest
from threading import Event

from c10net.tasks.task import Task

# stubbed class inheriting Task
class TaskStub(Task):
    def __init__(self, wait_event : Event = None):
        super().__init__({})
        self.wait_event = wait_event

    def start(self):
        self._state.set_progress(0.421)
        if self.wait_event:
            while (
                not self.wait_event.is_set() 
                and not self._state.terminate.is_set()
                and not self._state.finish.is_set()
                ):
                self._state.set_progress(0.421)

    def interrupt():
        raise KeyboardInterrupt


# factory fixture to allow parameterized construction of TaskStub
@pytest.fixture
def task_stub():
    def _create_task_stub(fake_work_done : Event = None):
        return TaskStub(fake_work_done)
    return _create_task_stub