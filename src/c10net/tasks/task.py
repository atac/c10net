
from c10net.tasks.worker import AbstractWorker

class Task(AbstractWorker):
    '''
    Abstract class to be implemented by tasks
    '''
    
    def __init__(self, cli_args : dict):
        '''
        Configure the task as needed with the CLI arguments. When 
        parallel is true, use multithreaded process when available.
        '''
        super().__init__()

        self._cli_args = cli_args 
        self._start_stage = None
        self._threads = []

    
    def _start_threads(self):
        for thread in self._threads:
            thread.start()
    
    def _join_threads(self):
        for thread in self._threads:
            thread.join()

    def _check_thread_is_alive(self):
        for thread in self._threads:
            if thread.is_alive():
                return True
        
        return False