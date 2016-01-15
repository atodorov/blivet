import unittest

from blivet.formats.fs import *
from blivet.size import Size

class FSOverheadTestCase(unittest.TestCase):

    def test_required_size_FS(self):
        # FS is abstract parent which doesn't have metadata
        self.assertEqual(FS.get_required_size(Size("100 MiB")), Size("100 MiB"))
        self.assertEqual(Ext2FS.get_required_size(Size("100 MiB")), Size(Decimal(Size("100 MiB")) / Decimal(0.93)))

    def test_biggest_overhead_FS(self):
        self.assertTrue(FS.biggest_overhead_FS() is BTRFS)
        self.assertTrue(FS.biggest_overhead_FS([FATFS, Ext2FS, Ext3FS, Ext4FS]) is Ext4FS)

        with self.assertRaises(ValueError):
            FS.biggest_overhead_FS([])

        # only classes with FS parent will be used
        with self.assertRaises(ValueError):
            class Dummy(object):
                pass

            FS.biggest_overhead_FS([Dummy])

