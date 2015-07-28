#!/usr/bin/env python3
# Copyright (c) 2015 Jonathan Dowland <jon@dowland.me>
# distributed under the terms of the GNU Public License (GPL) Version 2 only

import unittest, struct, io
from inkfoundry import parseinstr, getmap, verify_mapping

class TestInkFoundry(unittest.TestCase):
    def test_parseinstr_comments(self):
        comment_examples = ["# hi there","    # more comments" "", "#", "   "]
        self.assertEqual(parseinstr(comment_examples), ([], []))

    def test_parseinstr_mixedmaps(self):
        """Test an input file which mixes the input files and mapping
           declarations (which is not permitted)"""

        test = "zomg.wad\n0 0 31 0\nfoo.wad".split("\n")
        with self.assertRaises(Exception):
            parseinstr(test)

    def test_parseinstr_allgood(self):
        test = ["zomg.wad\n","0 0 31 0\n"]
        self.assertEqual(parseinstr(test), (["zomg.wad"],[[0,0,31,0]]))

    def test_parseinstr_shortmaps(self):
        test = ["zomg.wad\n","0 31 0\n"]
        self.assertEqual(parseinstr(test), (["zomg.wad","0 31 0"],[]))

    def test_getmap_lmp(self):
        with open('t/colormap.lmp','rb') as fh:
            lump = fh.read()
            fh.seek(0)
            self.assertEqual(getmap(fh), lump)

    def test_getmap_wad(self):
        with open('t/colormap.wad','rb') as fh:
            lump = getmap(fh)
            self.assertEqual(len(lump), 256*34)

    def test_getmap_iwad(self):
        """As above, but pretend it's an IWAD."""
        with open('t/colormap.wad','rb') as fh:
            wad = fh.read()
            iwad = io.BytesIO(b'I' + wad[1:])
            lump = getmap(iwad)
            self.assertEqual(len(lump), 256*34)

    def test_getmap_notwad(self):
        """As above, but corrupt the WAD magic. It will treat it as a raw lump"""
        with open('t/colormap.wad','rb') as fh:
            wad = fh.read()
            iwad = io.BytesIO(b'?' + wad[1:])
            lump = getmap(iwad)
            self.assertEqual(len(lump), 256*34)
            iwad.seek(0)
            self.assertEqual(lump, iwad.read(256*34))

    def test_getmap_emptywad(self):
        """A WAD without a COLORMAP lump"""
        fh = io.BytesIO(struct.pack('<4sllll8s', b'PWAD', 1, 12, 0, 12, b'VOIDLUMP'))
        with self.assertRaises(IOError):
            getmap(fh)

    def test_getmap_shortwad(self):
        """WAD with a COLORMAP lump which is too short"""
        fh = io.BytesIO(struct.pack('<4sll4sll8s', b'PWAD', 1, 12, b'CRAP', 4, 12, b'COLORMAP'))
        with self.assertRaises(IOError):
            getmap(fh)

    def test_getmap_truncwad(self):
        """WAD with a COLORMAP lump which claims to be the right length but isn't"""
        fh = io.BytesIO(struct.pack('<4sll4sll8s', b'PWAD', 1, 12, b'CRAP', 34*256, 12, b'COLORMAP'))
        with self.assertRaises(IOError):
            getmap(fh)

    def test_getmap_trunclmp(self):
        """Short lump"""
        fh = io.BytesIO(bytes(32))
        with self.assertRaises(IOError):
            getmap(fh)

    def test_getmap_longlump(self):
        """Long lump"""
        fh = io.BytesIO(bytes(35*256))
        lump = getmap(fh)
        self.assertEqual(34*256, len(lump))

    def test_verify_mapping_ok(self):
        sources = ['t/colormap.wad']
        self.assertIsNone(verify_mapping(sources, 0, 0, 33, 0))

    def test_verify_mapping_src_out_of_range(self):
        sources = ['t/colormap.wad']
        with self.assertRaises(Exception):
            verify_mapping(sources, 1,  0,  0,  0)

    def test_verify_mapping_dst_out_of_range(self):
        sources = ['t/colormap.wad']
        with self.assertRaises(Exception):
            verify_mapping(sources, 0, 34,  0,  0)
        with self.assertRaises(Exception):
            verify_mapping(sources, 0,  0, 34,  0)
        with self.assertRaises(Exception):
            verify_mapping(sources, 0,  0,  0, 34)

    def test_verify_mapping_range_too_large(self):
        sources = ['t/colormap.wad']
        with self.assertRaises(Exception):
            verify_mapping(sources, 0, 15,  0,  0)
        with self.assertRaises(Exception):
            verify_mapping(sources, 0,  0, 15, 19)

if __name__ == '__main__':
        unittest.main()
