#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import unittest

import json.decoder

import misc


_jsondirpath = os.path.join(misc.getscriptpath(__file__), "data", "service", "json")


class ServiceTests(unittest.TestCase):
    def setUp(self):
        import app.state
        app.state.initialized = True
        import app
        self.appmodule = app

    def init_services(self, jsonfile):
        json = os.path.join(_jsondirpath, jsonfile)
        return self.appmodule.ServiceManager(json)

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
        with self.assertRaises(Exception):
            self.init_services("noPaths.json")
