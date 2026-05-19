"""
Class providing structures and functions to manage passing data between task
stages.

A stage should create an instance of this class and use the provided 
functions to deposit processed data (unless final stage) and shutdown as 
needed.

An event passed at initialization is used to check termination conditions
during deposit and retrieval.
"""
from queue import Queue, Empty, Full, ShutDown
from threading import Event

class DataPipe:
    def __init__(self, terminate_event : Event, max_queue_size=10000):
        self.MAX_QUEUE_SIZE = max_queue_size
        self.RETRIEVAL_SIZE = int(self.MAX_QUEUE_SIZE / 2)

        self.terminate = terminate_event
        self._queue = Queue(maxsize=self.MAX_QUEUE_SIZE)
        
    def deposit(self, data : list):
        """
        Insert processed data into the queue.
        """
        for d in data:
            self._try_deposit(d)
    
    def retrieve(self):
        """
        Get any existing data from the queue. The instance owner should make
        thisfunction reference available to another object to be used as its
        data source.
        """
        return self._try_retrieve()
    
    def shutdown(self, immediate=False):
        self._queue.shutdown(immediate)

    def _try_deposit(self, data):
        """
        Attempt to deposit data to the queue. 

        If raises ShutDown, throw exception to caller
        If raises Full, wait increasing timeout up to max timeout
        Check events between attempts and return on terminate
        """
        MAX_TIMEOUT = 1024
        timeout = 1

        success = False

        while not success and not self.terminate.is_set():
            try:
                self._queue.put(data, True, timeout / 1000)
                success = True
            except Full:
                timeout = min(timeout * 2, MAX_TIMEOUT)
            except ShutDown as ex:
                ex.add_note("Attempted to deposit to a pipe that has been shut down")
                raise ex
                #raise BrokenPipeError("Attempted to deposit to a pipe that has been shut down")
            except Exception as ex:
                ex.add_note("Unknown exception occurred during deposit")
                raise ex

    def _try_retrieve(self):
        """
        Attempt to retrieve data from the queue. 

        If raises ShutDown or Empty, return available data or empty list.
        If ShutDown is raised with no data (closed), throw exception to caller.
        Check events between attempts and return on terminate.
        """
        data = []

        while not self.terminate.is_set() and len(data) < self._queue.maxsize:
            try:
                data.append(self._queue.get(False))
            except Empty:
                break
            except ShutDown as ex:
                if (len(data) == 0):
                    raise ex
                break
            except Exception as ex:
                ex.add_note("Unknown exception occurred during retrieval")
                raise ex
        
        return data

    def _debug_get_items_inserted(self):
        return self._debug_count

    # def is_empty(self):
    #     """Returns True if the queue is empty."""
    #     return self._queue.empty()
