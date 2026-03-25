
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
        self._task_func = None
