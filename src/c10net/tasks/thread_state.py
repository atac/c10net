
from threading import Event

class ThreadState:
    def __init__(self):
        self.terminate = Event()
        self.finish = Event()
        self.progress = 0.0
        pass

