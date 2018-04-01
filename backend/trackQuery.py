"""
Author: Pankhuri Kumar
"""

import environment
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.exceptions import NotFound
import sp_search

class trackQuery:

    def __init__(self, test=False):
        envData = environment.Data()

        config = envData.config['pyrebaseConfig']

        if test:
            localCredentials = credentials.Certificate(config['serviceAccount'])
            firebase_admin.initialize_app(localCredentials)

        self.database = firestore.client()
        self.artistReference = self.database.collection(u'artist_q')
        self.trackReference = self.database.collection(u'track_q')

        self.search = sp_search.sp_search()

    # TODO: Decide if we can query by genre or not
    # def searchArtists(self, choices):
    #
    #     genre = choices['genre_label']
    #     genreList = self.createGenreList(genre)
    #
    #     matchingArtists = self.artistReference.where(u'genre',)

    def searchTracks(self, choiceList):

        minRange, maxRange = self.setRanges(choiceList)
        unformatted_results = {}

        #TODO: querying if parameter is missing
        try:
            # First attempt to match exact results, inequality filters not allowed on multiple properties..
            query = self.trackReference.where(u'tempo', u'>=', minRange['tempo']).where(u'tempo', u'<=', maxRange['tempo']).where(u'key', u'==', choiceList['key_label']).where(u'time_signature', u'==', choiceList['time_sig_label']).limit(20)

            docs = query.get()

            for doc in docs:

                unformatted_results[doc.id] = doc.to_dict()

            """
            matchingTempo = self.trackReference.where(u'tempo', u'>=', minRange['tempo']).where(u'key', u'<=', maxRange['tempo']).limit(1).get()
            matchingKey = self.trackReference.where(u'key', u'>=', minRange['key']).where(u'key', u'<=', maxRange['key']).limit(1).get()
            matchingTS = self.trackReference.where(u'time_signature', u'>=', minRange['time_signature']).where(u'key', u'<=', maxRange['time_signature']).limit(1).get()
            """

        except NotFound:
            pass
        #TODO: equate results and add to results

        results = self.formatResults(unformatted_results)

        return results

    def setRanges(self, choiceList):
        #TODO: Add more features
        minRange = {}
        maxRange = {}

        if 'tempo_label' in choiceList:
            minRange['tempo'] = choiceList['tempo_label'] - 2
            maxRange['tempo'] = choiceList['tempo_label'] + 2
        else:
            minRange['tempo'] = 0
            maxRange['tempo'] = 500

        if 'key_label' in choiceList:
            minRange['key'] = choiceList['key_label'] - 1
            maxRange['key'] = choiceList['key_label'] + 1
        else:
            minRange['key'] = 0
            maxRange['key'] = 11

        if 'time_sig_label' in choiceList:
            minRange['time_signature'] = choiceList['time_sig_label'] - 0
            maxRange['time_signature'] = choiceList['time_sig_label'] + 0
        else:
            minRange['time_signature'] = 1
            maxRange['time_signature'] = 7

        return minRange, maxRange

    # TODO For now, we have to get the name of the artist from the artist_q. Mayabe we should put in track_q to speed things up?
    def formatResults(self, results):

        formatted_results = []

        # TODO Get the album photo since, for now, it is not in the database
        album_ids = [x['album_id'] for x in results.values()]
        album_list = self.search.albums(album_ids)
        albums = {}

        for album in album_list['albums']:
            albums[album['id']] = album['images'][1]['url']

        for song_id in results.keys():
            doc_ref = self.artistReference.document(u'{0}'.format(results[song_id]['artist_id']))
            artist = self.search.single_artist(results[song_id]['artist_id'])
            try:
                doc = doc_ref.get().to_dict()
                artist_name = artist['name']
                list = [results[song_id]['name'],
                        artist_name,
                        results[song_id]['tempo'],
                        results[song_id]['key'],
                        results[song_id]['time_signature'],
                        results[song_id]['danceability'],
                        results[song_id]['energy'],
                        results[song_id]['loudness'],
                        results[song_id]['speechiness'],
                        results[song_id]['acousticness'],
                        results[song_id]['instrumentalness'],
                        results[song_id]['liveness'],
                        results[song_id]['valence'],
                        albums[results[song_id]['album_id']]
                        ]
                formatted_results.append(list)

            except NotFound:
                pass

        return formatted_results

if __name__ == '__main__':

    # Testing

    input = {
        "tempo_label": 150,
        "key_label": 4,
        "time_sig_label": 4
    }

    test = trackQuery(True)
    print(test.searchTracks(input))
