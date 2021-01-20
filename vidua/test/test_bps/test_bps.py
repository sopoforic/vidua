import os

import pytest

from vidua import bps

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

valid_test_files = [
    ('test_a.bps', 'test_a_original.txt', 'test_a_modified.txt'),
    ('test_b.bps', 'test_b_original.txt', 'test_b_modified.txt'),
]

valid_test_files = [tuple(os.path.join(BASE_PATH, part)
                          for part in group)
                    for group in valid_test_files]


@pytest.mark.parametrize("bps_path", (f[0] for f in valid_test_files))
def test_validate(bps_path):
    with open(bps_path, 'rb') as bps_file:
        bps.validate_patch(bps_file)


def test_bps_a_get_info():
    with open(os.path.join(BASE_PATH, 'test_a.bps'), 'rb') as bps_file:
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


def test_apply_incompatible_source():
    with open(os.path.join(BASE_PATH, 'test_a.bps'), 'rb') as patch:
        with open(os.path.join(BASE_PATH, 'test_a_modified.txt'), 'rb') as original:
            with pytest.raises(ValueError) as excinfo:
                bps.patch(original, patch)
            assert str(excinfo.value).startswith('Incompatible source.')


def test_apply_failed_bad_checksum():
    with open(os.path.join(BASE_PATH, 'test_k.bps'), 'rb') as patch:
        with open(os.path.join(BASE_PATH, 'test_a_original.txt'), 'rb') as original:
            with pytest.raises(ValueError) as excinfo:
                bps.patch(original, patch)
            assert str(excinfo.value).startswith('Invalid checksum. Stored checksum')


def test_validate_wrong_format():
    with open(os.path.join(BASE_PATH, 'test_d.bps'), 'rb') as patch:
        with pytest.raises(ValueError) as excinfo:
            bps.validate_patch(patch)
        assert str(excinfo.value) == 'Invalid file format marker.'


def test_validate_too_small():
    with open(os.path.join(BASE_PATH, 'test_c.bps'), 'rb') as patch:
        with pytest.raises(ValueError) as excinfo:
            bps.validate_patch(patch)
        assert str(excinfo.value) == 'Patch too short.'


def test_validate_invalid_checksum():
    with open(os.path.join(BASE_PATH, 'test_e.bps'), 'rb') as patch:
        with pytest.raises(ValueError) as excinfo:
            bps.validate_patch(patch)
        assert 'Invalid checksum.' in str(excinfo.value)


def test_validate_invalid_source_size():
    with open(os.path.join(BASE_PATH, 'test_f.bps'), 'rb') as patch:
        with pytest.raises(ValueError) as excinfo:
            bps.validate_patch(patch)
        assert str(excinfo.value) == 'Failed to decode source size.'


def test_validate_invalid_target_size():
    with open(os.path.join(BASE_PATH, 'test_g.bps'), 'rb') as patch:
        with pytest.raises(ValueError) as excinfo:
            bps.validate_patch(patch)
        assert str(excinfo.value) == 'Failed to decode target size.'


def test_validate_invalid_metadata_size():
    with open(os.path.join(BASE_PATH, 'test_h.bps'), 'rb') as patch:
        with pytest.raises(ValueError) as excinfo:
            bps.validate_patch(patch)
        assert str(excinfo.value) == 'Failed to decode metadata size.'


def test_validate_invalid_metadata_size_overflow():
    with open(os.path.join(BASE_PATH, 'test_i.bps'), 'rb') as patch:
        with pytest.raises(ValueError) as excinfo:
            bps.validate_patch(patch)
        assert str(excinfo.value) == 'Metadata size too large.'


def test_validate_source_read_beyond_end():
    with open(os.path.join(BASE_PATH, 'test_j.bps'), 'rb') as patch:
        with pytest.raises(ValueError) as excinfo:
            bps.validate_patch(patch)
        assert str(excinfo.value).startswith('Attempted to read beyond end of source.')
