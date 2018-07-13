import os

import pytest

from vidua import bps

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

valid_test_files = [
    ('test_bps_a.bps', 'test_bps_a_original.txt', 'test_bps_a_modified.txt'),
    ('test_bps_b.bps', 'test_bps_b_original.txt', 'test_bps_b_modified.txt'),
]

valid_test_files = [tuple(os.path.join(BASE_PATH, part) for part in group) for group in valid_test_files]

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

@pytest.mark.parametrize("bps_path,original_path,modded_path", valid_test_files)
def test_apply(bps_path, original_path, modded_path):
    with open(bps_path, 'rb') as patch:
        with open(original_path, 'rb') as original:
            with open(modded_path, 'rb') as modded:
                assert bps.patch(original, patch).read() == modded.read()
