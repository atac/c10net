
class ProgressBar:
    def __init__(self, start, end):
        if (start >= end):
            raise ValueError()
        
        self._start = start
        self._end = end
        self._time_range = end - start
        self._progress = 0.0 # always stored in percent
        self._precision = 1

    def set_progress_relative(self, progress : float):
        """Set progress with a value within the range of start and end."""

        progress = self._clamp(progress)
            
        curr = progress - self._start

        percent = (curr / self._time_range) * 100.0
        percent = round(percent, self._precision)

        if (percent > self._progress):
            self._progress = percent

    def set_progress_absolute(self, progress : float):
        """Set progress with a value within the range of 0.0 and 1.0"""
        progress = self._clamp_abs(progress)

        percent = progress * 100.0

        if (percent > self._progress):
            self._progress = percent

    def get_bar(self):
        return self._generate_progress_bar()
    
    def _clamp(self, value : float):
        if value < self._start:
            return self._start
        elif value > self._end:
            return self._end
        else:
            return value
    
    def _clamp_abs(self, value : float):
        if value < 0.0:
            return 0.0
        elif value > 1.0:
            return 1.0
        else:
            return value


    def _generate_progress_bar(self):
        bar = '|'
        bar_size = 50

        fraction = int((self._progress / 100.0) * bar_size)

        for i in range(0, fraction):
            bar += '='
        
        for i in range(0, bar_size-fraction):
            bar += '-'

        bar += f'| {self._progress}%   '

        return bar

    
def _print_progress():
    progress_bar = _generate_progress_bar()
    print('\r' + progress_bar, end='')