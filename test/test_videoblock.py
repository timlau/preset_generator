import pytest

from generator.calc import VideoBlock, BlockType


@pytest.fixture
def block():
    return VideoBlock(0, 0, 100, 200)


@pytest.fixture
def qhd():
    return VideoBlock(0, 0, 3840, 2160)


def test_iadd(block):
    block += VideoBlock(10, 20, 100, 200)
    assert block.x == 10
    assert block.y == 20
    assert block.width == 200
    assert block.height == 400


def test_add():
    block = VideoBlock(10, 20, 100, 200) + VideoBlock(10, 20, 100, 200)
    assert block.x == 20
    assert block.y == 40
    assert block.width == 200
    assert block.height == 400


def test_padding(block):
    block.set_padding(10)
    assert block.x == 10
    assert block.y == 10
    assert block.width == 80
    assert block.height == 180


def test_scale(qhd: VideoBlock):
    qhd.scale(0.5)
    assert qhd.x == 0
    assert qhd.y == 0
    assert qhd.width == 1920
    assert qhd.height == 1080


def test_scale_center():
    block = VideoBlock(0, 0, 200, 200)
    block.scale(0.5, center=True)
    assert block.x == 50
    assert block.y == 50
    assert block.width == 100
    assert block.height == 100


def test_move_to_corner(qhd: VideoBlock):
    block = VideoBlock(50, 50, 200, 200)
    block.move_to_corner(qhd, BlockType.TopLeft)
    assert block.x == 0
    assert block.y == 0
    block.move_to_corner(qhd, BlockType.TopRight)
    assert block.x == 3640
    assert block.y == 0
    block.move_to_corner(qhd, BlockType.BottomLeft)
    assert block.x == 0
    assert block.y == 1960
    block.move_to_corner(qhd, BlockType.BottomRight)
    assert block.x == 3640
    assert block.y == 1960


def test_split(qhd):
    blocks: list[VideoBlock] = list(qhd.split(2, 2))
    assert len(blocks) == 4
    assert blocks[0].x == 0
    assert blocks[0].y == 0
    assert blocks[0].width == 1920
    assert blocks[0].height == 1080
    assert blocks[1].x == 1920
    assert blocks[1].y == 0
    assert blocks[1].width == 1920
    assert blocks[1].height == 1080
    assert blocks[2].x == 0
    assert blocks[2].y == 1080
    assert blocks[2].width == 1920
    assert blocks[2].height == 1080
    assert blocks[3].x == 1920
    assert blocks[3].y == 1080
    assert blocks[3].width == 1920
    assert blocks[3].height == 1080


def test_copy(qhd: VideoBlock):
    new_block: VideoBlock = qhd.copy()
    assert id(qhd) != id(new_block)
    assert qhd.x == new_block.x
    assert qhd.y == new_block.y
    assert qhd.width == new_block.width
    assert qhd.height == new_block.height
