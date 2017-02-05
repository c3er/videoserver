#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json.decoder
import unittest

import app
import misc


_jsondirpath = os.path.join(misc.getscriptpath(__file__), "data", "service", "json")


class ServiceTests(unittest.TestCase):
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
        with self.assertRaises(json.decoder.JSONDecodeError):
            self.init_services("malformed1.json")

    def test_no_paths(self):
        with self.assertRaises(AssertionError):
            self.init_services("noPaths.json")

    def test_no_common_path(self):
        with self.assertRaises(app.URLError):
            self.init_services("noCommonPathBase.json")

    def test_service_can_be_declared_only_once(self):
        with self.assertRaises(AssertionError):
            self.init_services("double.json")
