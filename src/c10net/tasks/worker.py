
from abc import ABC, abstractmethod

from c10net.tasks.thread_state import ThreadState


class WorkerConfigError(Exception):
    '''Raised when a configuration error is detected within a task.'''
    def __init__(self, msg : str):
        super().__init__()

        if len(msg) > 0:
            super().add_note(msg)


class AbstractWorker(ABC):
    def __init__(self):
        self._state = ThreadState()
        self._stages = []

    def terminate(self):
        '''Set the state.terminate Event on this and subtasks.'''
        self._state.terminate.set()
        for stage in self._stages:
            stage.terminate()

    def finished(self):
        '''Returns true when state.finished Event is set.'''
        return self._state.finished.is_set()

    def progress(self):
        '''Returns state.progress'''
        return self._state.progress
    

    @abstractmethod
    def start(self):
        '''Spawn the configured processes, update progress, join all subtasks, and set the state.finished Event'''
        pass
