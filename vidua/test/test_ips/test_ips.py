import os

import pytest

from vidua import ips

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

valid_test_files = [
    ('test_a.ips', 'test_a_original.txt', 'test_a_modified.txt'),
    ('test_b.ips', 'test_b_original.txt', 'test_b_modified.txt'),
]

valid_test_files = [tuple(os.path.join(BASE_PATH, part)
                          for part in group)
                    for group in valid_test_files]


@pytest.mark.parametrize("ips_path", (f[0] for f in valid_test_files))
def test_validate(ips_path):
    with open(ips_path, 'rb') as ips_file:
        ips.validate_patch(ips_file)


@pytest.mark.parametrize("ips_path,original_path,modded_path", valid_test_files)
def test_apply(ips_path, original_path, modded_path):
    with open(ips_path, 'rb') as patch:
        with open(original_path, 'rb') as original:
            with open(modded_path, 'rb') as modded:
                assert ips.patch(original, patch).read() == modded.read()
