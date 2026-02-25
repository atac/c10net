
from c10net.tasks import parse_chapter10 as pc


def test_set_filters():
    # set filters empty -> passes everything
    pc._set_filter_parameters([], [])
    assert pc._passes_filter(1, 2)

    # restrict ids
    pc._set_filter_parameters([3], [])
    assert not pc._passes_filter(1, 2)
    assert pc._passes_filter(3, 2)

    # restrict types
    pc._set_filter_parameters([], [7])
    assert not pc._passes_filter(3, 2)
    assert pc._passes_filter(3, 7)

    # restrict both
    pc._set_filter_parameters([3], [7])
    assert not pc._passes_filter(3, 2)
    assert not pc._passes_filter(1, 7)
    assert pc._passes_filter(3, 7)

def test_pass_setup_packet():
    # pass setup packet when flag set
    pc._set_filter_parameters([3], [7], pass_setup_packet=True)
    assert pc._passes_filter(0, 1)