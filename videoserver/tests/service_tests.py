#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json.decoder
import unittest

import app
import misc


_jsondirpath = os.path.join(misc.getscriptpath(__file__), "data", "service", "json")


class ServiceTests(unittest.TestCase):
    def init_error(self, exctype, jsonfile):
        with self.assertRaises(exctype):
            self.init_services(jsonfile)

    def init_services(self, jsonfile):
        json = os.path.join(_jsondirpath, jsonfile)
        return app.ServiceManager(jsonpath=json)

    def test_smoke(self):
        services = self.init_services("simple.json")
        self.assertGreaterEqual(len(services), 1, "Services in simple case could be initialized")

    def test_empty(self):
        noservice = self.init_services("empty.json")
        self.assertEqual(len(noservice), 0, "Empty JSON file can be loaded")

    def test_malformed_json_syntax(self):
        self.init_error(json.decoder.JSONDecodeError, "malformed1.json")

    def test_no_paths(self):
        self.init_error(AssertionError, "noPaths.json")

    def test_no_common_path(self):
        self.init_error(app.URLError, "noCommonPathBase.json")

    def test_service_can_be_declared_only_once(self):
        self.init_error(AssertionError, "double.json")

    def test_url_does_not_begin_with_slash(self):
        self.init_error(app.URLError, "invalidPath1.json")


if __name__ == '__main__':
    unittest.main()
