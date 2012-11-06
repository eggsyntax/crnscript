'''
Created on May 11, 2011

@author: egg.davis
'''
import doctest
import unittest

import data, domainquery, graph, observation, output, utils

suite = unittest.TestSuite()
suite.addTest(doctest.DocTestSuite(data))
suite.addTest(doctest.DocTestSuite(domainquery))
suite.addTest(doctest.DocTestSuite(graph))
suite.addTest(doctest.DocTestSuite(observation))
suite.addTest(doctest.DocTestSuite(output))
suite.addTest(doctest.DocTestSuite(utils))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
