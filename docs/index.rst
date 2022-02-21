.. vidua documentation master file, created by
   sphinx-quickstart on Fri Jul 13 09:14:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to vidua's documentation!
=================================

Vidua can be used to apply (IPS or BPS) patches. It is intended particularly for use with ROM
hacks.

Usage
-----

A simple script is included to validate or apply patches from the command line:

.. code-block:: console

    vidua patch.bps original.rom patched_output.rom

Full usage instructions:

.. code-block:: console

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


Vidua may also be used as a library, to validate or apply patches from within
another program::

    from vidua import bps
    
    patch = open('patch.bps', 'rb')
    original = open('original.rom', 'rb')
    
    with open('patched.rom', 'wb') as patched:
        patched.write(bps.patch(original, patch).read())


If the file is very large, you may prefer to use :py:func:`copyfileobj <shutil.copyfileobj>` when
writing to disk.

Credits
-------

Alcaro's `Floating IPS <https://www.smwcentral.net/?p=section&a=details&id=11474>`_
was very useful in working out how to handle BPS files when byuu's documentation
was unclear.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   vidua
   bps

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

