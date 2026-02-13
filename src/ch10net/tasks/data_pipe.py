"""
Class providing structures and functions to manage the throughput of data in 
a task

A task module should create an instance of this class and use the provided 
functions to retrieve from the source pipe, process the data, and optionally 
deposit to a sink pipe provided at initialization.

An event passed at initialization is used to check termination conditions
during deposit and retrieval.
"""
from queue import Queue, Empty, Full
from threading import Event

class DataPipe:
    def __init__(self, terminate_event : Event, max_queue_size=10000):
        self.MAX_QUEUE_SIZE = max_queue_size
        self.RETRIEVAL_SIZE = int(self.MAX_QUEUE_SIZE / 2)

        self.terminate = terminate_event
        self._queue = Queue(maxsize=self.MAX_QUEUE_SIZE)
    
    def deposit(self, data : list):
        """Called by the instance owner from a function that can be referenced
        as the sink function for another DataPipe instance."""
        for d in data:
            if not self.terminate.is_set():
                try:
                    self._queue.put(d)
                except Exception:
                    print("Error depositing data to queue")
                    self.terminate.set()
    
    def retrieve(self):
        """Used by the instance owner to retrieve source data from the queue
        for processing."""
        data = []
        
        if not self.terminate.is_set():
                for i in range(self.RETRIEVAL_SIZE):
                    try:
                        data.append(self._queue.get_nowait())
                    except Empty:
                        break
                    except Exception:
                        print("Error retrieving data from queue")
                        self.terminate.set()
        
        return data

    def is_empty(self):
        """Returns True if the queue is empty."""
        return self._queue.empty()