"""
Author: Erin Riglin
"""

import sys
import os.path
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'tests')))

ignore_file = "ignore_tests.txt"
directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'tests'))
print(directory)

"""Enter the names of modules in tests folder to omit"""
no_include = open(os.path.join(directory, ignore_file), 'r').read().splitlines()

modules = [x.strip('.py') for x in os.listdir(os.path.join(os.path.dirname(__file__), os.path.pardir, 'tests'))
              if x.endswith('.py') and x not in no_include]

""" Inspects the code folder and gets the class of each module to run tests """
suite = []
for module_name in modules:
    module = __import__(module_name)
    suite += unittest.TestLoader().loadTestsFromModule(module)

""" Add unit tests to test suite and run """
alltests = unittest.TestSuite(suite)
test_runner = unittest.TextTestRunner(verbosity=2).run(alltests)

