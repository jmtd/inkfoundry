# InkFoundry suite

InkFoundry will eventually be a suit of tools for manipulating Doom `COLORMAP` lumps.

Right now, InkFoundry is a simple command-line tool that can be used to remix
Doom `COLORMAP` lumps.  It is inspired by the program MIXMAPS which was
distributed with INKWORKS.

Copyright (c) Jonathan Dowland, 2015. Distributed under the terms of the GNU GPL,
version 2. See LICENSE for full details.

## Usage

    inkfoundry instructions.txt <outfile.wad>

if `outfile.wad` is not supplied, the output filename will be the input file with
the suffix changed to `.wad`.

The instructions language is inspired by and similar - but not identical - to that used
by mixmaps. It's slightly more powerful.

Empty lines, all-whitespace lines, lines which begin with a hash ('#') symbol, or lines
which have some whitespace and then have a hash symbol, are treated as comments and are
ignored.

The first non-comment lines should list, one per line, input files. These can be either
raw `COLORMAP` lumps or Doom WAD files (IWAD or PWAD).

The remaining lines are the remix directives. Each line should be four integers divided
by whitespace. e.g.

    0 0 33 0

The integers have the following meanings:

1. The first one is an index into the input files, beginning with 0. So, the line above
   refers to the first input file supplied.

2. The second one is the start of a range to pick from the input file. In the example
   above, we're defining a range from the first entry, the full-bright color-map. (The
   ranges start from 0).

3. The third one is the end of the input range. There are 34 mappings in a `COLORMAP`
   lump, so 33 is the index for the last one. The input range we've defined above is
   therefore the entire `COLORMAP`.

4. The fourth one is an offset into the output `COLORMAP` to put the range. We've selected
   0, so the entire line simply copies the whole `COLORMAP` from the first input file
   into the output.

## More interesting example

    colormap.lmp
    lavamap.lmp
    0   0 33  0
    0  31 31 30
    1   0  0 31

The above example has two input colormaps: `colormap.lmp` is Doom's default and
`lavamap.lmp` is a lava-tinted mapping (generated using `colormap.py` from the
Freedoom sources, by Colin Phipps. Thanks!)

The first directive copies the entirety of the default `COLORMAP`.

The second takes the darkest mapping and writes it one mapping earlier.

The final directive takes the brightest mapping from the second input,
`lavamap.lmp`, and puts it in the darkest slot of the output.

## Future work

Currently we've only cloned MIXMAPS. It would be nice to clone INKWORKS too, and/or
add some other useful tools for manipulating `COLORMAP`s.

## See also

<http://jmtd.net/doom/>
<http://doomwiki.org/wiki/Inkworks>
<http://doomwiki.org/wiki/COLORMAP>
<http://freedoom.github.io/>
