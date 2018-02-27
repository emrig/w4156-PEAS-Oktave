import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'code')))


from sp_search import sp_search
import unittest

class SearchTest(unittest.TestCase):
    """This class uses the Spotify Search to test the response
    returned by the Spotify API in sp_search.py"""

    def setUp(self):
        self.search = sp_search()

    def test_limit(self):
        limitCases = [('Michael', 4, 4),
                      ('Bob', 10, 10)]
        list(map(lambda x: self.push_assertLimit(x[0], x[1], x[2]), limitCases))

    def test_invalidLimit(self):
        invalidCase = 12345
        self.push_assertInvalid(invalidCase)

    def test_type(self):
        typeCases = [('Michael', 'genres', list),
                     ('Bob', 'href', unicode),
                     ('Tina', 'external_urls', dict),
                     ('Michael', 'followers', dict),
                     ('Bob', 'images', list),
                     ('Tina', 'name', unicode),
                     ('Michael', 'popularity', int),
                     ('Bob', 'type', unicode),
                     ('Tina', 'uri', unicode)]
        list(map(lambda x: self.push_assertType(x[0], x[1], x[2]), typeCases))

    def test_zeroLength(self):
        lenCases = [('Stiarway', 0),
                    ('sdjasrtawidfj', 0),
                    ('46529347', 0)]
        list(map(lambda x: self.push_assertZero(x[0], x[1]), lenCases))

    def push_assertLimit(self, searchString, limit, returnLength):
        results = self.search.artist(searchString, limit)
        result = results['artists']['items']
        self.assertEqual(len(result), returnLength)

    def push_assertInvalid(self, searchString):
        self.assertRaises(Exception, self.search.artist(searchString))

    def push_assertType(self, searchString, field, responseType):
        results = self.search.artist(searchString)
        result = results['artists']['items']
        for r in result:
            self.assertEqual(type(r[field]), responseType)

    def push_assertZero(self, searchString, responseLength):
        results = self.search.artist(searchString)
        result = results['artists']['items']
        self.assertEqual(len(result), responseLength)


if __name__ == '__main__':
    unittest.main()
