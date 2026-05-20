
import sys
from threading import Thread

from c10net.tasks.task import Task
from c10net.functions.progress_bar import ProgressBar

class Watchdog():
    def __init__(self, task : Task):
        self._task = task
        self._pb = ProgressBar(0.0, 1.0)
        self._message = ''

    def start(self):
        """
        Start the Task provided at initialization, and perform Watchdog
        responsibilities
            - report progress
            - terminate on error or user request
            - join all running threads
        """
        thread = Thread(target=self._task.start)
        thread.start()
        print('Task started...')

        self._enter_run_loop(thread)
            
        self.terminate()
            
        thread.join(5.0)

        if (not thread.is_alive()):
            print("\nDone")
        else:
            print("\nFailed to terminate task in time. Force quitting.")
            sys.exit(1)

    def terminate(self):
        """
        Call terminate on the running task. The effect is to cleanly
        exit as quickly as possible.
        """
        self._task.terminate()

    # def finish(self):
    #     """
    #     Call finish on the running task. The effect is to finish
    #     current data in processing stages and exit.
    #     """
    #     self._task.finish()

    def _enter_run_loop(self, thread : Thread):
        reenter = True

        while reenter: # reentry loop
            try:
                while thread.is_alive():
                    self._print_output()
                reenter = False

            except KeyboardInterrupt:
                reenter = not self._prompt_for_terminate()

            except Exception as err:
                print('An unknown error occurred')
                raise err


    def _print_output(self):
        debug = False

        if (debug):
            print(f'\r{self._task._debug_stages()}  {self._message}', end='')
        else:
            print(f'\r{self._get_bar()}    {self._message}', end='')

    def _get_bar(self):
        progress = self._task.progress()
        self._pb.set_progress_absolute(progress)
        return self._pb.get_bar()
    
    def _prompt_for_terminate(self):
        self._message = 'Terminate task? y/n (n): '
        self._print_output()
        self._message = '                         '
        user_input = input()
        if user_input:
            match user_input[0]:
                case 'y' | 'Y':
                    return True
                case _:
                    return False
        else:
            return False