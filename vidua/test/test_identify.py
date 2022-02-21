import os

import pytest

from vidua import PatchType, identify

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

test_files = [
    ('test_ips/test_a.ips', PatchType.IPS),
    ('test_ips/test_b.ips', PatchType.IPS),
    ('test_bps/test_a.bps', PatchType.BPS),
    ('test_bps/test_b.bps', PatchType.BPS),
    ('__init__.py', None),
]

test_files = [(os.path.join(BASE_PATH, f[0]), f[1]) for f in test_files]


@pytest.mark.parametrize("patch_file,patch_type", test_files)
def test_identify(patch_file, patch_type):
    with open(patch_file, 'rb') as patch_file:
        assert identify(patch_file) == patch_type
