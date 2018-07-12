import os

import pytest

from varipatch import bps

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

valid_test_files = [
    ('test_bps_a.bps', 'test_bps_a_original.txt', 'test_bps_a_modified.txt'),
    ('test_bps_b.bps', 'test_bps_b_original.txt', 'test_bps_b_modified.txt'),
]

@pytest.mark.parametrize("bps_patch_file", (f[0] for f in valid_test_files))
def test_validate(bps_patch_file):
    with open(os.path.join(BASE_PATH, bps_patch_file), 'rb') as bps_file:
        bps.validate_patch(bps_file)

def test_bps_a_get_info():
    with open(os.path.join(BASE_PATH, 'test_bps_a.bps'), 'rb') as bps_file:
        info = bps.patch_info(bps_file)
        assert info['source_size'] == 37
        assert info['target_size'] == 24
        assert info['metadata'] == b''
        assert info['source_checksum'] == 0xcbc5f68d
        assert info['final_checksum'] == 0x9dde9720

@pytest.mark.parametrize("bps_patch_file,original_file,modified_file", valid_test_files)
def test_apply(bps_patch_file, original_file, modified_file):
    with open(os.path.join(BASE_PATH, bps_patch_file), 'rb') as bps_patch:
        with open(os.path.join(BASE_PATH, original_file), 'rb') as original:
            with open(os.path.join(BASE_PATH, modified_file), 'rb') as modified:
                assert bps.patch(original, bps_patch).read() == modified.read()
