# vidua

Vidua can be used to apply patches. It is intended particularly for use with ROM
hacks.

## Supported patch formats

* BPS
* IPS

## Usage

A simple script is included to validate or apply patches from the command line:

```shell
vidua patch.bps original.rom patched_output.rom
```

Full usage instructions:

```shell
$ vidua --help
usage: vidua [-h] [-v] [-q] PATCH [ORIGINAL] [OUTPUT]

Apply or validate patches.

positional arguments:
  PATCH           the patch file
  ORIGINAL        the file to be patched
  OUTPUT          filename to write patched file

optional arguments:
  -h, --help      show this help message and exit
  -v, --validate  validate the patch only; do not apply it
  -q, --quiet     suppress output except errors
```

Vidua may also be used as a library, to validate or apply patches from within
another program:

```python
from vidua import bps

patch = open('patch.bps', 'rb')
original = open('original.rom', 'rb')

with open('patched.rom', 'wb') as patched:
    patched.write(bps.patch(original, patch).read())
```

If the file is very large, you may prefer to use `shutil.copyfileobj` when
writing to disk.

## Credits

Alcaro's [Floating IPS](https://www.smwcentral.net/?p=section&a=details&id=11474)
was very useful in working out how to handle BPS files when byuu's documentation
was unclear.

[![Build Status](https://travis-ci.org/sopoforic/vidua.svg?branch=master)](https://travis-ci.org/sopoforic/vidua)
