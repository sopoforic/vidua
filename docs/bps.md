# BPS notes

Documentation on this format from byuu can be found
[here](https://www.romhacking.net/documents/746/). I compared my understanding
of that document to what Floating IPS actually does, and found my understanding
lacking. I'll record here some clarifications.

## Relative offsets

Regarding relative offsets, byuu writes:

> beat patches keep track of the current file offsets in both the source and
> target files separately. Reading from either increments their respective
> offsets automatically.

The exact behavior here wasn't clear to me, but at length I came to three major
conclusions:

1. A `SourceRead` **does not** increment the source offset, even though you are
    clearly reading from the source. You do the copy and then seek back to where
    you started.
2. A `SourceCopy` **does** increment the source offset, so the new offset will be
    `old_offset + relative_offset + copy_length`.
3. A `TargetCopy` **is not** specified relative to the current output position,
    but to a separate target file reading pointer, which starts at zero (and is
    only modified by `TargetCopy` operations).

## Checksums

Checksums are little-endian.

