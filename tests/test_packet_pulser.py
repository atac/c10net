import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import c10net.functions.packet_pulser as pp


def test_packet_pulser_interval(monkeypatch):
    # Simulate time progression: creation time then a later time past interval
    times = [100.0, 101.0, 103.0]

    def fake_time():
        return times.pop(0)

    monkeypatch.setattr(pp.time, 'time', fake_time)

    dummy = object()
    p = pp.PacketPulser(dummy)
    p.set_interval(2.0)

    # Now call check_pulse() — fake_time returns 101.0 now, interval should not pass
    pkt = p.check_pulse()
    assert not pkt

    # Next call gets 103.0, interval passes
    pkt = p.check_pulse()
    assert pkt is dummy

