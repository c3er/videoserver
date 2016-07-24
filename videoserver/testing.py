#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import unittest
import tempfile

import app


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        app.web.config['TESTING'] = True
        self.app = app.web.test_client()

    def test_smoke(self):
        self.assertNotEqual(self.app, None, "Application testing initialized")


if __name__ == '__main__':
    unittest.main()