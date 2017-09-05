#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import re

import app
import misc


class ApplicationTestClassBase(unittest.TestCase):
    dir = "data/"
    file = "data/video.mp4"

    def setUp(self):
        app.web.config['TESTING'] = True
        app.rootpath = misc.getscriptpath(__file__)
        self.app = app.web.test_client()

    def assertResponse(self, response , code, condition, msg=""):
        self.assertEqual(response.status_code, code, "Response code is {}".format(code))
        self.assertTrue(condition, msg)

    def response(self, service, param=""):
        url = "/{}/{}".format(service, param)
        return url, self.app.get(url)


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

    # XXX Currently it is not possible to test that a proper HTML,
    # containing an exception stacktrace is rendered

    # def test_internal_server_error(self):
    #     url, response = self.response("exception")
    #     data = response.data.decode("utf-8")
    #     self.assertResponse(
    #         response,
    #         500,
    #         "error" in data and "Traceback (most recent call last):" in data,
    #         "An internal server error leads to an exception message"
    #     )


class FileListTests(ApplicationTestClassBase):
    def dirresponse(self, param):
        return self.response("files", param)

    def test_filelist(self):
        url = "/files/"
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200, 'Given URL "{}" is responded with status "200 OK"'.format(url))

    def test_unknown_parameter(self):
        param = "this-has-to-be-unknown"
        url, response = self.dirresponse(param)
        self.assertResponse(response, 404, param in response.data.decode("utf-8"), "Returned HTML contains given unknown parameter")

    def test_dir_parameter(self):
        url, response = self.dirresponse(self.dir)
        self.assertResponse(response, 200, self.dir in response.data.decode("utf-8"), "Returned HTML contains given directory parameter")

    def test_links_have_proper_urls(self):
        url, response = self.dirresponse(self.dir)
        matches = [
            match
            for match in re.findall(r'href="(.*)"', response.data.decode("utf-8"))
            if match.strip()
        ]
        self.assertResponse(response, 200, len(matches) != 1, "Returned HTML contains proper links")

    def test_file_parameter(self):
        url, response = self.dirresponse(self.file)
        self.assertResponse(response, 302, self.file in response.data.decode("utf-8"), "Returned HTML contains given file parameter")


class FileViewTests(ApplicationTestClassBase):
    def file_response(self, param):
        return self.response("fileview", param)

    def test_no_parameter(self):
        url, response = self.file_response("")
        self.assertEqual(response.status_code, 302, "Response code is 302")

    def test_unknown_parameter(self):
        param = "some-unknown-file"
        url, response = self.file_response(param)
        self.assertResponse(response, 404, param in response.data.decode("utf-8"), "Returned HTML contains given unknown parameter")

    def test_file_parameter(self):
        url, response = self.file_response(self.file)
        self.assertResponse(response, 200, self.file in response.data.decode("utf-8"), "Returned HTML contains given file parameter")


class FileContentTests(ApplicationTestClassBase):
    def content_response(self, param):
        return self.response("filecontent", param)

    def test_content_can_be_retreived(self):
        url, response = self.content_response(self.file)
        self.assertResponse(response, 200, len(response.data) > 0, "File content can be retreived")

    def test_unknown_parameter(self):
        param = "some-unknown-file"
        url, response = self.content_response(param)
        self.assertResponse(response, 404, param in response.data.decode("utf-8"), "Returned HTML contains given unknown parameter")

    def test_dir_parameter(self):
        url, response = self.content_response(self.dir)
        self.assertResponse(response, 400, self.dir in response.data.decode("utf-8"), "Returned HTML contains given directory parameter")


if __name__ == '__main__':
    unittest.main()
