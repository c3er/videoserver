#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import unittest
import tempfile

import app
import misc


class ApplicationTestClassBase(unittest.TestCase):
    def setUp(self):
        app.web.config['TESTING'] = True
        app.rootpath = misc.getscriptpath(__file__)
        self.app = app.web.test_client()

    def assertResponse(self, response , code, condition, msg=""):
        self.assertEqual(response.status_code, code, "Response code is {}".format(code))
        self.assertTrue(condition, msg)


class ApplicationTests(ApplicationTestClassBase):
    def test_smoke(self):
        self.assertNotEqual(self.app, None, "Application testing initialized")

    def test_unknown_parameter(self):
        url = "/this-has-to-be-unknown"
        response = self.app.get(url)
        self.assertEqual(response.status_code, 404, 'Given URL "{}" is responded with status "404 Not Found"'.format(url))

    def test_urls(self):
        pages = [
            app.services.foo,
            app.services.dirlisting,
            app.services.fileview,
        ]
        for page in pages:
            self.assertTrue(misc.islistlike(page.urls), "Page object contains a list of URLs")
            self.assertTrue(page.func is not None, "Page object has a handler")


class FileListTests(ApplicationTestClassBase):
    dir = "tests/data"
    file = "tests/data/test.gif"

    def dirresponse(self, param):
        url = "/files/" + param
        return url, self.app.get(url)

    def test_filelist(self):
        for url in ("/", "/files/", "/files/" + self.dir):
            response = self.app.get(url)
            self.assertEqual(response.status_code, 200, 'Given URL "{}" is responded with status "200 OK"'.format(url))

    def test_unknown_parameter(self):
        param = "this-has-to-be-unknown"
        url, response = self.dirresponse(param)
        self.assertResponse(response, 404, param in response.data.decode("utf-8"), "Returned HTML contains given parameter")

    def test_dir_parameter(self):
        url, response = self.dirresponse(self.dir)
        self.assertResponse(response, 200, self.dir in response.data.decode("utf-8"), "Returned HTML contains given parameter")

    def test_file_parameter(self):
        url, response = self.dirresponse(self.file)
        self.assertResponse(response, 302, self.file in response.data.decode("utf-8"), "Returned HTML contains given parameter")


class FileViewTests(ApplicationTestClassBase):
    def file_response(self, param):
        url = "/fileview/" + param
        return url, self.app.get(url)

    def test_no_parameter(self):
        url, response = self.file_response("")
        self.assertEqual(response.status_code, 302, "Response code is 302")

    def test_unknown_parameter(self):
        param = "some-unknown-file"
        url, response = self.file_response(param)
        self.assertResponse(response, 404, param in response.data.decode("utf-8"), "Returned HTML contains given parameter")


if __name__ == '__main__':
    unittest.main()