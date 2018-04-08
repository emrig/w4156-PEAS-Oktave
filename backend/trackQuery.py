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

    def __init__(self, test=False, verbose=False):
        envData = environment.Data()

        config = envData.config['pyrebaseConfig']
        self.test = test
        self.verbose = verbose

        if self.test:
            localCredentials = credentials.Certificate(config['serviceAccount'])
            try:
                firebase_admin.initialize_app(localCredentials)
            except:
                None

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

        if self.verbose:
            print("[searchTracks] choiceList:{0}".format(choiceList))

        minRange, maxRange = self.setRanges(choiceList)
        results = []

        #TODO: querying if parameter is missing
        try:
            # First attempt to match exact results, inequality filters not allowed on multiple properties..
            query = self.trackReference.where(u'tempo', u'>=', minRange['tempo']).where(u'tempo', u'<=', maxRange['tempo']).where(u'key', u'==', choiceList['key_label']).where(u'time_signature', u'==', choiceList['time_sig_label']).limit(20)

            docs = query.get()

            for doc in docs:

                json = doc.to_dict()
                json[u'track_id'] = doc.id
                results.append(json)

            """
            matchingTempo = self.trackReference.where(u'tempo', u'>=', minRange['tempo']).where(u'key', u'<=', maxRange['tempo']).limit(1).get()
            matchingKey = self.trackReference.where(u'key', u'>=', minRange['key']).where(u'key', u'<=', maxRange['key']).limit(1).get()
            matchingTS = self.trackReference.where(u'time_signature', u'>=', minRange['time_signature']).where(u'key', u'<=', maxRange['time_signature']).limit(1).get()
            """

        except NotFound:
            pass
        #TODO: equate results and add to results

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


if __name__ == '__main__':

    # Testing

    input = {
        "tempo_label": 150,
        "key_label": 4,
        "time_sig_label": 4
    }

    test = trackQuery(True)
    print(test.searchTracks(input))
