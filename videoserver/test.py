#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest


def main():
    testcases = unittest.TestLoader().discover('tests', '*tests.py')
    suite = unittest.TestSuite(testcases)
    runner = unittest.TextTestRunner()
    runner.run(suite)
    

if __name__ == '__main__':
    main()
