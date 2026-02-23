import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import c10net.functions.progress_bar as pb

def test_progress_bar_prints(capsys):
    pb.set_bounds(0.0, 100.0)
    pb.update_progress(50.0)
    captured = capsys.readouterr()
    assert '===' in captured.out
    assert '---' in captured.out
    assert '%' in captured.out

def test_progress_bar_updates(capsys):
    pb.set_bounds(0.0, 100.0)

    pb.update_progress(0.0)
    pb._print_progress()
    captured = capsys.readouterr()
    assert '0.0%' in captured.out

    pb.update_progress(50.0)
    pb._print_progress()
    captured = capsys.readouterr()
    assert '50.0%' in captured.out

    pb.update_progress(100)
    pb._print_progress()
    captured = capsys.readouterr()
    assert '100.0%' in captured.out
    