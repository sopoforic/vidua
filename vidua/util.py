from enum import Enum
from typing import BinaryIO


class PatchType(Enum):
    IPS = 1
    BPS = 2


def identify(patch: BinaryIO):
    """Identify the type of a patch.

    :param patch: the patch file
    """
    patch.seek(0)
    if patch.read(4) == b'BPS1':
        return PatchType.BPS
    patch.seek(0)
    if patch.read(5) == b'PATCH':
        return PatchType.IPS
    return None


def copy_bytes(from_buffer: BinaryIO, to_buffer: BinaryIO, length: int, size: int = 2**8):
    """Copy bytes from one buffer to another.

    :param from_buffer: the source buffer
    :param to_buffer: the destination buffer
    :param length: the total number of bytes to copy
    :param size: the number of bytes to copy at once
    """
    while length > 0:
        length -= to_buffer.write(from_buffer.read(min(length, size)))
