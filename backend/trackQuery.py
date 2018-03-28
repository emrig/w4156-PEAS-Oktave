"""
Author: Pankhuri Kumar
"""

import environment
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.exceptions import NotFound

class trackQuery:

    def __init__(self):
        envData = environment.Data()

        config = envData.config['pyrebaseConfig']
        localCredentials = credentials.Certificate(config['serviceAccount'])
        firebase_admin.initialize_app(localCredentials)
        self.database = firestore.client()
        self.artistReference = self.database.collection(u'artist_q')
        self.trackReference = self.database.collection(u'track_q')

    # TODO: Decide if we can query by genre or not
    # def searchArtists(self, choices):
    #
    #     genre = choices['genre_label']
    #     genreList = self.createGenreList(genre)
    #
    #     matchingArtists = self.artistReference.where(u'genre',)

    def searchTracks(self, choiceList):

        minRange, maxRange = self.setRanges(choiceList)
        results = []

        for i in range(0, 5):
            #TODO: querying if parameter is missing
            try:
                matchingTempo = self.trackReference.where(u'tempo', u'>=', minRange['tempo']).where(u'key', u'<=', maxRange['tempo']).limit(1).get()
                matchingKey = self.trackReference.where(u'key', u'>=', minRange['key']).where(u'key', u'<=', maxRange['key']).limit(1).get()
                matchingTS = self.trackReference.where(u'time_signature', u'>=', minRange['time_signature']).where(u'key', u'<=', maxRange['time_signature']).limit(1).get()
            except NotFound:
                pass
            #TODO: equate results and add to results

        return results

    def setRanges(self, choiceList):
        #TODO: Add more features
        minRange = {}
        maxRange = {}

        if 'tempo_label' in choiceList:
            minRange['tempo'] = choiceList['tempo_label'] - 10
            maxRange['tempo'] = choiceList['tempo_label'] + 10
        else:
            minRange['tempo'] = 0
            maxRange['tempo'] = 500

        if 'key_label' in choiceList:
            minRange['key'] = choiceList['key'] - 1
            maxRange['key'] = choiceList['key'] + 1
        else:
            minRange['key'] = 0
            maxRange['key'] = 12

        if 'time_sig_label' in choiceList:
            minRange['time_signature'] = choiceList['time_sig_label'] - 2
            maxRange['time_signature'] = choiceList['time_sig_label'] + 2
        else:
            minRange['time_signature'] = 1
            maxRange['time_signature'] = 9

        return minRange, maxRange

