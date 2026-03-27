
from abc import ABC, abstractmethod

from c10net.tasks.thread_state import ThreadState


class WorkerConfigError(Exception):
    """Raised when a configuration error is detected within a task."""
    def __init__(self, msg : str):
        super().__init__()

        if len(msg) > 0:
            super().add_note(msg)


class AbstractWorker(ABC):
    def __init__(self):
        self._state = ThreadState()
        self._stages = []

    def terminate(self):
        """Set the state.terminate Event on this and subtasks."""
        self._state.terminate.set()
        for stage in self._stages:
            stage.terminate()

    def finish(self):
        """Set the state.finish Event on this and subtasks."""
        self._state.finish.set()
        for stage in self._stages:
            stage.finish()

    def progress(self):
        """
        Returns state._progress under Lock, guaranteed to be between
        0.0 and 1.0
        """
        return self._state.get_progress()
    

    @abstractmethod
    def start(self):
        """
        Spawn the configured processes, update progress, join all
        subtasks, and set the state.finished Event.
        """
        pass
