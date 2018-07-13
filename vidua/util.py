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
