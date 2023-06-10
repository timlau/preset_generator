from generator.calc import BlockType


def test_block():
    names = [enum.name for enum in BlockType]
    assert names == ["TopLeft", "TopRight", "BottomLeft", "BottomRight"]
