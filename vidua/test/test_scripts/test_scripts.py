import os
import pytest
import tempfile


def test_script(script_runner):
    ret = script_runner.run('vidua', '--help')
    assert ret.success
    assert 'usage:' in ret.stdout
    assert ret.stderr == ''


BASE_PATH = os.path.dirname(os.path.realpath(__file__))

valid_test_files = [
    'test_ips/test_a.ips',
    'test_ips/test_b.ips',
    'test_bps/test_a.bps',
    'test_bps/test_b.bps',
]

valid_test_files = [os.path.join(BASE_PATH, '..', name)
                    for name in valid_test_files]


@pytest.mark.parametrize("file_path", valid_test_files)
def test_validate(file_path, script_runner):
    ret = script_runner.run('vidua', '-v', file_path)
    assert ret.success
    assert ret.stderr == 'vidua: INFO: The patch file is valid.\n'
    assert ret.stdout == ''


def test_validate_quiet(script_runner):
    ret = script_runner.run('vidua', '-v', '-q', valid_test_files[0])
    assert ret.success
    assert ret.stderr == ''
    assert ret.stdout == ''


invalid_test_files = [
    'test_scripts.py',
    '../__init__.py',
]

invalid_test_files = [os.path.join(BASE_PATH, name)
                      for name in invalid_test_files]


@pytest.mark.parametrize("file_path", invalid_test_files)
def test_validate_invalid(file_path, script_runner):
    ret = script_runner.run('vidua', '-v', file_path)
    assert not ret.success
    assert ret.stdout == ''
    assert 'vidua: error: The patch file is not of a supported type.' in ret.stderr


def test_validate_invalid_quiet(script_runner):
    ret = script_runner.run('vidua', '-v', '-q', invalid_test_files[0])
    assert not ret.success
    assert ret.stdout == ''
    assert 'vidua: error: The patch file is not of a supported type.' in ret.stderr


patch_test_files = [
    ('test_a.ips', 'test_a_original.txt', 'test_a_modified.txt'),
    ('test_b.ips', 'test_b_original.txt', 'test_b_modified.txt'),
]

patch_test_files = [tuple(os.path.join(BASE_PATH, '..', 'test_ips', part)
                          for part in group)
                    for group in patch_test_files]


@pytest.mark.parametrize("ips_path,original_path,modded_path", patch_test_files)
def test_apply(ips_path, original_path, modded_path, script_runner):
    with tempfile.TemporaryDirectory() as d:
        ret = script_runner.run(
            'vidua', ips_path, original_path, os.path.join(d, 'output'))
        assert ret.success
        assert ret.stdout == ''
        assert ret.stderr == ''
        with open(os.path.join(d, 'output'), 'rb') as output:
            with open(modded_path, 'rb') as modded:
                assert output.read() == modded.read()
