import pytest

from generator.plugins import GridCalculator


@pytest.fixture
def calc() -> GridCalculator:
    return GridCalculator(2, 2)


def test_block_width(calc: GridCalculator):
    assert calc.block_width == 1920


def test_block_height(calc: GridCalculator):
    assert calc.block_height == 1080


# TopLeft
def test_calc_block_1(calc: GridCalculator):
    x, y, w, h = calc.calc_block(0, 0, 1, 1)
    assert x == 16
    assert y == 16
    assert w == 1904
    assert h == 1064


# TopRight
def test_calc_block_2(calc: GridCalculator):
    x, y, w, h = calc.calc_block(0, 1, 1, 1)
    print(x, y, w, h)
    assert x == 1936
    assert y == 16
    assert w == 1888
    assert h == 1064


# BottomLeft
def test_calc_block_3(calc: GridCalculator):
    x, y, w, h = calc.calc_block(1, 0, 1, 1)
    print(x, y, w, h)
    assert x == 16
    assert y == 1096
    assert w == 1904
    assert h == 1048


# BottomRight
def test_calc_block_4(calc: GridCalculator):
    x, y, w, h = calc.calc_block(1, 1, 1, 1)
    print(x, y, w, h)
    assert x == 1936
    assert y == 1096
    assert w == 1888
    assert h == 1048


# TopLeft
def test_calc_no_border_top_left(calc: GridCalculator):
    x, y, w, h = calc.calc_block(0, 0, 1, 1, border=False)
    assert x == 0
    assert y == 0
    assert w == 1920
    assert h == 1080


# BottomRight
def test_calc_no_border_bottom_right(calc: GridCalculator):
    x, y, w, h = calc.calc_block(1, 1, 1, 1, border=False)
    assert x == 1920
    assert y == 1080
    assert w == 1920
    assert h == 1080
