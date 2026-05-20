
from collections.abc import Callable, abstractmethod

from c10net.tasks.worker import AbstractWorker
from c10net.stages.data_pipe import DataPipe

class StagePipeError(Exception):
    def __init__(self, msg : str):
        super().__init__()
        self.add_note(msg)

class Stage(AbstractWorker):
    '''
    Abstract class to be implemented by task stages.
    '''
    def __init__(self, source : Callable = None, direct_link : Callable = None):
        '''
        source : 
            For parallel stages. This should be a source data_pipe's retrieve function.

        direct_link : 
            For sequential stages. This should be the next stage's direct_input function.
        '''
        super().__init__()

        self._pipe = DataPipe(self._state.terminate)
        self.retrieve = source
        self.deposit = direct_link if direct_link is not None else self._pipe.deposit
        
    def pipe_output(self):
        """
        Returns a function reference to be used by the next stage in sequence 
        to retrieve processed data from this stage.
        """
        #return self._pipe.retrieve
        raise StagePipeError("Pipe output not implemented for this Stage")
    
    def direct_input(self):
        """
        Returns a function reference used for direct input into this stage.
        Function should process all input data before returning.
        """
        #return self._process
        raise StagePipeError("Direct input not implemented for this Stage")
