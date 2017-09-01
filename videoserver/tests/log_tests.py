#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import os

import log
import misc


_logfile = os.path.join(misc.getscriptpath(__file__), "data", "tmp", "test.log")


class LogTests(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(_logfile)
        except FileNotFoundError:
            pass
        log.init(_logfile, debug_on=True, use_console=False)

    def tearDown(self):
        log.close()
        self.assertFalse(log.isready(), "Logger is closed")

    def getlogdata(self):
        with open(_logfile, encoding="utf8") as f:
            return f.read()

    def logmessage(self, logmethod, msg):
        logmethod(msg)
        self.assertTrue(msg in self.getlogdata(), 'Message "{}" can be logged'.format(msg))

    def test_isready(self):
        self.assertTrue(log.isready(), "Logger is initialized")

    def test_log_info(self):
        self.logmessage(log.info, "Info message")

    def test_log_debug(self):
        self.logmessage(log.debug, "Debug message")

    def test_log_error(self):
        self.logmessage(log.error, "Error message")

    def test_log_exception(self):
        self.logmessage(log.exception, "Exception message")

    def test_log_debug_deactivated(self):
        msg = "Debug message that should not appear"
        log.close()
        log.init(_logfile, debug_on=False, use_console=False)
        log.debug(msg)
        self.assertFalse(msg in self.getlogdata(), 'Message "{}" is not logged'.format(msg))


if __name__ == '__main__':
    unittest.main()
