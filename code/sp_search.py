import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sp_dev_key import SPOTIFY_CLIENT_ID
from sp_dev_key import SPOTIFY_CLIENT_SECRET

"""
Refer to https://spotipy.readthedocs.io/en/latest/#api-reference 
for Spotipy API reference
"""

class sp_search:
    def __init__(self):

        CLIENT_ID = SPOTIFY_CLIENT_ID
        CLIENT_SECRET = SPOTIFY_CLIENT_SECRET

        self.client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

    def artist(self, artist_name, limit=None):

        spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        result = spotify.search(q='artist:' + str(artist_name), limit=limit, type='Artist')

        return result

if __name__ == '__main__':

    # Use this for local testing, reference for how this works
    model = sp_search()
    results = model.artist("Michael", 10)

    results_list = results['artists']['items']

    for result in results_list:

        print((result['name'], result['id'], result['popularity'], result['type']))
