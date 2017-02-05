#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

import app
import misc


class FileBasicsTests(unittest.TestCase):
    def setUp(self):
        app.rootpath = misc.getscriptpath(__file__)

        self.dirpath = "data"
        self.filepath = "data/test.gif"

        self.dirobject = app.fs.getfile(self.dirpath)
        self.fileobject = app.fs.getfile(self.filepath)

    def test_root(self):
        file = app.fs.getfile("")
        self.assertIsInstance(file, app.fs.FileObject, "Object for root directory can be created")

    def test_directory_object_level1(self):
        self.assertTrue(self.dirpath in self.dirobject.url, "Object with 1 membered path can be created")

    def test_directory_object_level2(self):
        path = "data/subdir"
        file = app.fs.getfile(path)
        self.assertTrue(path in file.url, "Object with 2 membered path can be created")

    def test_file_object(self):
        self.assertTrue(self.filepath in self.fileobject.url, "Object with file path can be created")

    def test_directory_url(self):
        url = app.services.dirlisting.urlbase + self.dirpath
        self.assertEqual(url, self.dirobject.url, "Known URL is " + url)

    def test_file_url(self):
        url = app.services.fileview.urlbase + self.filepath
        self.assertEqual(url, self.fileobject.url, "Known URL is " + url)

    def test_ospath_does_not_contain_backslashes(self):
        dirpath = self.dirobject.ospath
        filepath = self.fileobject.ospath
        self.assertTrue("\\" not in dirpath + filepath, "There is no backslash in OS paths")


if __name__ == '__main__':
    unittest.main()
