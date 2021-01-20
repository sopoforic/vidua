from enum import Enum


class PatchType(Enum):
    IPS = 1
    BPS = 2


def identify(patch):
    patch.seek(0)
    if patch.read(4) == b'BPS1':
        return PatchType.BPS
    patch.seek(0)
    if patch.read(5) == b'PATCH':
        return PatchType.IPS
    return None


def copy_bytes(from_buffer, to_buffer, length, size=2**8):
    while length > 0:
        length -= to_buffer.write(from_buffer.read(min(length, size)))
