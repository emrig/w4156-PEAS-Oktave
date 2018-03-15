"""
Author: Alexandra Taylor-Gutt
"""

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'backend')))


from sp_search import sp_search
import unittest

class SearchTest(unittest.TestCase):
    """This class uses the Spotify Search to test the response
    returned by the Spotify API in sp_search.py"""

    def setUp(self):
        self.search = sp_search()

    def test_type(self):
        typeCases = [('Michael', 'external_urls', str),
                     ('Tina', 'external_urls', int),
                     ('Michael', 'followers', bool)
                     ]
        list(map(lambda x: self.push_assertType(x[0], x[1], x[2]), typeCases))

    def push_assertType(self, searchString, field, responseType):
        results = self.search.artist(searchString)
        result = results['artists']['items']
        for r in result:
            self.assertNotEqual(type(r[field]), responseType)


if __name__ == '__main__':
    unittest.main()
