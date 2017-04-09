#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

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

    def test_root_url(self):
        for url in "", "/":
            response = self.app.get(url)
            self.assertTrue(response.status_code in (301, 302), "Calling the root URL causes a redirection")

    def test_unknown_parameter(self):
        url = "/this-has-to-be-unknown"
        response = self.app.get(url)
        self.assertEqual(response.status_code, 404, 'Given URL "{}" is responded with status "404 Not Found"'.format(url))

    def test_services_are_available(self):
        counter = 0
        for service in app.services:
            counter += 1
        self.assertGreater(counter, 0, "There is any service registered and it is possible to iterate through them")

    def test_urlbase_starts_with_slash(self):
        for service in app.services:
            urlbase = service.urlbase
            self.assertTrue(urlbase.startswith("/"), "URL '{}' starts with '/'".format(urlbase))

    def test_services_contain_url_lists(self):
        for service in app.services:
            self.assertTrue(misc.islistlike(service.urls), "Service object contains a list of URLs")

    def test_services_have_handler(self):
        for service in app.services:
            self.assertTrue(service.func is not None, "Service object has a handler")


class FileListTests(ApplicationTestClassBase):
    dir = "data"
    file = "data/test.gif"

    def dirresponse(self, param):
        url = "/files/" + param
        return url, self.app.get(url)

    def test_filelist(self):
        url = "/files/"
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


class VideoTests(ApplicationTestClassBase):
    pass


if __name__ == '__main__':
    unittest.main()
