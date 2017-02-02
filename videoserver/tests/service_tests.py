#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import unittest

import misc


_jsondirpath = os.path.join(misc.getscriptpath(__file__), "data", "service", "json")


class ServiceTests(unittest.TestCase):
    def setUp(self):
        import app.state
        app.state.initialized = True
        import app
        self.appmodule = app

    def test_smoke(self):
        simple_json = os.path.join(_jsondirpath, "simple.json")
        services = self.appmodule.ServiceManager(simple_json)
        self.assertGreaterEqual(len(services), 1, "Services in simple case could be initialized")
