
from c10net.tasks.worker import AbstractWorker, WorkerConfigError

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

        try:
            self._init()

            if self._cli_args['parallel']:
                self._setup_parallel()
            else:
                self._setup_linear()
        except KeyError as err:
            raise WorkerConfigError("Required parameters not found") from err
        
    def _init(self):
        """
        Override to perform any initialization before stage setup.
        """
        pass

    def start(self):
        """
        Start threads/stages and update progress until finished or terminated.
        """
        if self._start_stage is None:
            raise WorkerConfigError("Worker not configured")
        
        self._start_threads()

        while (self._check_thread_is_alive()
               and not self._state.terminate.is_set()
               ):
            self._state.set_progress(self._start_stage.progress())
        
        self._join_threads()
    
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