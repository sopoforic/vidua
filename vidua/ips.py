from io import BytesIO
from typing import BinaryIO


def validate_patch(ips_patch: BinaryIO):
    """Verify that ``ips_patch`` is a valid BPS patch.

    If the patch is valid, return. If the patch is invalid, raise a
    ``ValueError`` describing the problem.

    :param ips_patch: the patch file
    """
    ips_patch.seek(0)
    header = ips_patch.read(5)
    if header != b'PATCH':
        raise ValueError("Invalid patch header.")

    while True:
        pos = ips_patch.tell()
        offset = ips_patch.read(3)
        if len(offset) < 3:
            raise ValueError("Ran out of data in IPS patch file. Offset: 0x{:X}".format(pos))
        if offset == b'EOF':
            break

        offset = int.from_bytes(offset, byteorder='big')
        size = int.from_bytes(ips_patch.read(2), byteorder='big')

        if size == 0:
            # RLE
            pos = ips_patch.tell()
            if int.from_bytes(ips_patch.read(2), byteorder='big') == 0:
                raise ValueError("Zero size for IPS RLE record. Offset: 0x{:X}".format(pos))
            pos = ips_patch.tell()
            if len(ips_patch.read(1)) != 1:
                raise ValueError("Ran out of data in IPS patch file. Offset: 0x{:X}".format(pos))
        else:
            pos = ips_patch.tell()
            if len(ips_patch.read(size)) < size:
                raise ValueError("Ran out of data in IPS patch file. Offset: 0x{:X}".format(pos))

    post_end = ips_patch.read(4)
    if post_end and len(post_end) != 3:
        raise ValueError("Data past end of IPS file.")


def patch(source: BinaryIO, ips_patch: BinaryIO) -> BinaryIO:
    """Return the patched source.

    :param source: the source file to be patched
    :param ips_patch: the patch file
    """
    validate_patch(ips_patch)
    ips_patch.seek(5)

    source.seek(0)
    output = BytesIO(source.read())
    output.seek(0)

    while True:
        offset = ips_patch.read(3)
        if offset == b'EOF':
            break

        offset = int.from_bytes(offset, byteorder='big')
        output.seek(offset)
        size = int.from_bytes(ips_patch.read(2), byteorder='big')

        if size == 0:
            # RLE
            size = int.from_bytes(ips_patch.read(2), byteorder='big')
            value = ips_patch.read(1)
            output.write(value*size)
        else:
            value = ips_patch.read(size)
            output.write(value)

    post_end = ips_patch.read(3)
    if post_end:
        end = int.from_bytes(post_end, byteorder='big')
        output.seek(0, 2)
        if end > output.tell():
            raise ValueError("Tried to truncate file, but file was too short.")
        else:
            output.truncate(end)

    output.seek(0)
    return output
