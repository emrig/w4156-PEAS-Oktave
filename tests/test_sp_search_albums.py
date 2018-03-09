import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'code')))


from sp_search import sp_search
import unittest

class AlbumSearchTest(unittest.TestCase):
    """This class uses the Spotify Search to test the response
    returned by the Spotify API for albums by artist in sp_search.py"""

    def setUp(self):
        self.search = sp_search()
        self.artist = self.search.artist('Drake', 1)["artists"]["items"][0]

        self.artist_id = self.artist["id"]
        self.artist_name = self.artist["name"]

    def test_limit(self):
        limitCases = [(self.artist_id, 4, 4),
                      (self.artist_id, 10, 10)]
        list(map(lambda x: self.push_assertLimit(x[0], x[1], x[2]), limitCases))

    def test_invalidID(self):
        lenCases = ['Stiarway',
                    'sdjasrtawidfj',
                    6529347]
        list(map(lambda x: self.push_assertInvalid(x), lenCases))

    def test_type(self):
        typeCases = [(self.artist_id, 'album_type', unicode),
                     (self.artist_id, 'artists', list),
                     (self.artist_id, 'external_urls', dict),
                     (self.artist_id, 'available_markets', list),
                     (self.artist_id, 'images', list),
                     (self.artist_id, 'name', unicode),
                     (self.artist_id, 'uri', unicode)]
        list(map(lambda x: self.push_assertType(x[0], x[1], x[2]), typeCases))

    def push_assertLimit(self, searchString, limit, returnLength):
        results = self.search.artist_albums(searchString, limit=limit)
        result = results['items']
        self.assertLessEqual(len(result), returnLength)

    def push_assertInvalid(self, searchString):
        with self.assertRaises(Exception): self.search.artist_albums(searchString)

    def push_assertType(self, searchString, field, responseType):
        results = self.search.artist_albums(searchString)
        result = results['items']
        for r in result:
            self.assertEqual(type(r[field]), responseType)



if __name__ == '__main__':
    unittest.main()
