import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sp_dev_key import SPOTIFY_CLIENT_ID
from sp_dev_key import SPOTIFY_CLIENT_SECRET

"""
Refer to https://spotipy.readthedocs.io/en/latest/#api-reference 
for Spotipy API reference

If you want specific IDs for artists, albums, etc. Check out the shared spreadsheet on Google docs.
"""

class sp_search:
    def __init__(self):

        CLIENT_ID = SPOTIFY_CLIENT_ID
        CLIENT_SECRET = SPOTIFY_CLIENT_SECRET

        self.client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

    """
    We will use the artist search function to essentially 'crawl' through artists and their songs.
    This will return attributes for artist results (up to a limit). Maybe initially, to only focus on popular music,
    we can limit the scope of our database to only 'popular' artists above a certain 'popularity' metric.
    """

    def artist(self, artist_name, limit=None):

        spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        result = spotify.search(q='artist:' + str(artist_name), limit=limit, type='Artist')

        return result

    """
    Returns a list of albums from an artist given the artist ID
    
    OPTIONAL:
    album_type - album, single, appears_on, compilation
    
    """
    def artist_albums(self, artist_id, album_type=None, limit=None):

        spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        result = spotify.artist_albums(artist_id, album_type=album_type, limit=limit)

        return result

    """
    Returns a list of tracks  from an artist given the artist ID
    
    OPTIONAL:
    album_type - album, single, appears_on, compilation
    
    """

    def album_tracks(self, album_id, limit=None):

        spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        result = spotify.album_tracks(album_id, limit=limit)

        return result

    """
    Takes a LIST of track IDs and returns the audio features
    """

    def audio_features(self, tracks):

        spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        result = spotify.audio_features(tracks)

        return result



if __name__ == '__main__':

    # Use this for local testing, reference for how this works

    model = sp_search()
    artist_results = model.artist("Michael", 5)
    artist_results_list = artist_results['artists']['items']

    for result in artist_results_list:
        print((result['name'], result['id'], result['popularity'], result['type']))

    #Albums for first artist
    album_results = model.artist_albums(artist_results_list[0]['id'])
    album_results_list = album_results['items']

    for album in album_results_list:
        print((album['name'], album['release_date'], album['id']))

    #Songs for the first album

    track_results = model.album_tracks(album_results_list[0]['id'])
    print(track_results)
    track_results_list = track_results['items']

    for track in track_results_list:
        print((track['name'], track['id']))

    #Song features for tracks

    track_ids = [str(x['id']) for x in track_results_list]
    audio_features_results_list = model.audio_features(track_ids)

    for audio_feature in audio_features_results_list:
        print((audio_feature['id'], audio_feature['key'], audio_feature['tempo'], audio_feature['time_signature']))
