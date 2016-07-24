#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import unittest
import tempfile

import app
import app.misc


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        app.web.config['TESTING'] = True
        app.rootpath = app.misc.getscriptpath(__file__)
        self.app = app.web.test_client()

    def test_smoke(self):
        self.assertNotEqual(self.app, None, "Application testing initialized")

    def test_filelist(self):
        for url in ("/", "/files/", "/files/foobar"):
            response = self.app.get(url)
            self.assertEqual(response.status_code, 200, 'Given URL "{}" is responded with status "200 OK"'.format(url))

    def test_filelist_with_parameter(self):
        parameter = "foobar"
        response = self.app.get("/files/" + parameter)
        self.assertTrue(parameter in response.data.decode("utf-8"), "Returned HTML contains given parameter")


if __name__ == '__main__':
    unittest.main()