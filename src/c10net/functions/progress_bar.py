
_start = 0.0
_end = 0.0
_progress = 0


def set_bounds(start, end):
    global _start, _end

    _start = start
    _end = end


def update_progress(current: float):
    global _progress, _start, _end

    time_range = _end - _start
    curr = current - _start

    percent = (curr / time_range) * 100.0

    if (int(percent > _progress)):
        _progress = int(percent)
        _print_progress()
    
def _print_progress():
    progress_bar = _generate_progress_bar()
    print('\r' + progress_bar, end='')

def _generate_progress_bar():
    global _progress

    bar = '|'

    bar_size = 50

    fraction = int((_progress / 100.0) * bar_size)

    for i in range(0, fraction):
        bar += '='
    
    for i in range(0, bar_size-fraction):
        bar += '-'

    bar += f'| {_progress}%   '

    return bar
