
from collections.abc import Callable, abstractmethod

from c10net.tasks.worker import AbstractWorker
from c10net.tasks.data_pipe import DataPipe

class StageInputError(Exception):
    def __init__(self, msg : str):
        super().__init__()
        self.add_note(msg)

class Stage(AbstractWorker):
    '''
    Abstract class to be implemented by task stages.
    '''
    def __init__(self, sink : Callable = None):
        '''
        source : a DataPipe from which to retrieve data to process
        '''
        super().__init__()

        self._pipe = DataPipe(self._state.terminate)
        self._deposit = sink
        
    def pipe_input(self):
        """
        Returns a function reference used for depositing data input
        into the internal data pipe.
        """
        #return self._pipe.deposit
        raise StageInputError("Pipe input not implemented for this Stage")
    
    def direct_input(self):
        """
        Returns a function reference used for direct input into stage.
        Function should run stage on all input data before returning.
        """
        #return self._process
        raise StageInputError("Direct input not implemented for this Stage")
