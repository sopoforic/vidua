# vidua

Vidua can be used to apply patches. It is intended particularly for use with ROM
hacks.

## Supported patch formats

* BPS
* IPS

## Usage

Vidua is meant as a library, and does not yet have any convenience functions for
use as a script. It can presently be used to apply patches thus:

```python
from vidua import bps

patch = open('patch.bps', 'rb')
original = open('original.rom', 'rb')

with open('patched.rom', 'wb') as patched:
    patched.write(bps.patch(original, patch).read())
```

## Credits

Alcaro's [Floating IPS](https://www.smwcentral.net/?p=section&a=details&id=11474)
was very useful in working out how to handle BPS files when byuu's documentation
was unclear.

[![Build Status](https://travis-ci.org/sopoforic/vidua.svg?branch=master)](https://travis-ci.org/sopoforic/vidua)
