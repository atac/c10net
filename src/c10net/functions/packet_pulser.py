import time

from chapter10 import packet

class SetupPacketPulse:
    def __init__(self, setup_packet : packet):
        self._interval_s = 1.0
        self._last_pulse_time = time.time()
        self._packet = setup_packet

    def set_interval(self, interval : float):
        self._interval_s = interval
    
    def get_pulse(self):
        time_s = time.time()
        if (self._is_past_time_interval(time_s)):
            self._last_pulse_time = time_s
            return self._packet
        else:
            return None
        
    def _is_past_time_interval(self, time_s : float):
        return (time_s - self._last_pulse_time) > self._interval_s