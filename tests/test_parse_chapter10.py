
from c10net.tasks.parse_chapter10 import ParseChapter10


def test_set_filters_none():
    # set filters empty -> passes everything
    pc = ParseChapter10("test", [], [])
    assert pc._passes_filter(1, 2)

def test_set_filters_ids():
    # restrict ids
    pc = ParseChapter10("test", [3], [])
    assert not pc._passes_filter(1, 2)
    assert pc._passes_filter(3, 2)

def test_set_filters_types():
    # restrict types
    pc = ParseChapter10("test", [], [7])
    assert not pc._passes_filter(3, 2)
    assert pc._passes_filter(3, 7)

def test_set_filters_ids_and_types():
    # restrict both
    pc = ParseChapter10("test", [3], [7])
    assert not pc._passes_filter(3, 2)
    assert not pc._passes_filter(1, 7)
    assert pc._passes_filter(3, 7)

def test_pass_setup_packet():
    # pass setup packet when flag set
    pc = ParseChapter10("test", [3], [7], pass_setup_packet=True)
    assert pc._passes_filter(0, 1)