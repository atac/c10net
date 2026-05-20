import time

from chapter10 import Packet

class PacketPulser:
    def __init__(self):
        self._interval_s = 1.0
        self._last_pulse_time = time.time()
        self._packet = None

    def set_interval(self, interval : float):
        self._interval_s = interval
    
    def set_packet(self, packet : Packet):
        self._packet = packet
    
    def check_pulse(self):
        time_s = time.time()
        if (self._is_past_time_interval(time_s)):
            self._last_pulse_time = time_s
            return self._packet
        else:
            return None
        
    def _is_past_time_interval(self, time_s : float):
        if (self._packet is None):
            return False
        return (time_s - self._last_pulse_time) > self._interval_s