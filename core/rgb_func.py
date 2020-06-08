import itertools

from PIL import ImageColor


def rgb_hash_a(string: str) -> tuple:  # AndrewKing's formula
    hash_ = 0
    for i in string:
        hash_ = ord(i) + ((hash_ << 5) - hash_)
    c = format(hash_ & 0x00FFFFFF, 'x').upper()
    return ImageColor.getrgb("#{}".format("00000"[0: 6 - len(c)] + c))


def rgb_hash_v(source: str) -> tuple:  # Viktor's formula
    def add_with_max(init: int, val: int) -> int:
        return init + val if init + val < 256 else init + val - 256

    it = zip((b for b in source.encode()), itertools.cycle([0, 1, 2]))
    start = [0, 0, 0]
    for b, c in it:
        start[c] = add_with_max(start[c], b)

    return tuple(start)
