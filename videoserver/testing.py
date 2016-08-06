#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import unittest
import tempfile

import app
import misc


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        app.web.config['TESTING'] = True
        app.rootpath = misc.getscriptpath(__file__)
        self.app = app.web.test_client()

    def file_response(self, param):
        url = "/files/" + param
        return url, self.app.get(url)

    def error_response(self):
        return self.file_response("this-has-to-be-unknown")

    def test_smoke(self):
        self.assertNotEqual(self.app, None, "Application testing initialized")

    def test_filelist(self):
        for url in ("/", "/files/", "/files/app"):
            response = self.app.get(url)
            self.assertEqual(response.status_code, 200, 'Given URL "{}" is responded with status "200 OK"'.format(url))

    def test_filelist_with_dir_parameter(self):
        parameter = "app"
        url, response = self.file_response(parameter)
        self.assertTrue(parameter in response.data.decode("utf-8"), "Returned HTML contains given parameter")

    def test_filelist_with_file_parameter(self):
        parameter = "testing.py"
        url, response = self.file_response(parameter)
        self.assertTrue(parameter in response.data.decode("utf-8"), "Returned HTML contains given parameter")

    def test_filelist_wth_unknown_parameter(self):
        url, response = self.error_response()
        self.assertEqual(response.status_code, 404, 'Given URL "{}" is responded with status "404 Not Found"'.format(url))


if __name__ == '__main__':
    unittest.main()