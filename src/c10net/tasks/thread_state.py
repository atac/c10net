
from threading import Event, Lock

class ThreadState:
    def __init__(self):
        self.terminate = Event()
        #self.finish = Event()
        self._progress = 0.0
        self._progress_lock = Lock()
        pass

    def set_progress(self, progress : float):
        """
        Set the progress value after aquiring the lock.

        Raises ValueError if progress not in range of 0.0 and 1.0
        """
        if progress < 0.0 or progress > 1.0:
            raise ValueError
        
        with self._progress_lock:
            self._progress = progress
        
    def get_progress(self):
        """
        Get the progress after aquiring the Lock.

        Returns progress as a float between 0.0 and 1.0
        """
        with self._progress_lock:
            return self._progress