"""
Author: Pankhuri Kumar, Erin Riglin
"""

import environment
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# from google.cloud import firestore
from google.cloud.exceptions import NotFound
import sp_search
import os


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

        self.searchAlgConfig = envData.config['searchAlg']
        #TODO: setup credentials for this
        self.database = firestore.client()
        self.artistReference = self.database.collection(u'artist_q')
        self.trackReference = self.database.collection(u'track_q')

        self.search = sp_search.sp_search()

    def searchTracks(self, choiceList, songInfo=None):

        if self.verbose:
            print("[searchTracks] choiceList:{0}".format(choiceList))

        minRange, maxRange = self.setRanges(choiceList)
        results = []

        # Collect results based on +/-
        for attribute in self.searchAlgConfig['plusMinus'].keys():
            if attribute in choiceList.keys():

                try:

                    # TODO decide limit
                    query = self.trackReference.where(attribute, u'>=', minRange[attribute]).where(attribute, u'<=', maxRange[attribute]).limit(200)

                    docs = query.get()

                    for doc in docs:
                        result = doc.to_dict()
                        result[u'track_id'] = doc.id

                        # Calculate score based on weights
                        score = 0.0
                        for attribute in choiceList.keys():
                            
                            # TODO omit results that have a very similar name: saw results with [song name] original, [song name] remastered, etc.
                            # TODO omit zero values for now and missing attibutes.. log instead?
                            # TODO maybe filter very short songs, this would mean adding track length to DB
                            try:
                                if choiceList[attribute] != 0 and attribute in result:
                                    # filter attributes with more than 100% difference
                                    difference = max(0, 1 - abs((choiceList[attribute] - result[attribute]) / (choiceList[attribute])))
                                    score += difference * self.searchAlgConfig['weights'][attribute]

                            except:
                                pass

                        if (score, result) not in results:
                            clean_result = self.format_result(result)
                            results.append((score, clean_result))

                except NotFound:
                    pass

        results.sort(key=lambda x: x[0], reverse=True)

        if songInfo:
            ranked_results = [x[1] for x in results if x[0] >= self.searchAlgConfig['max_accuracy']]
        else:
            ranked_results = [x[1] for x in results]

        # Collect genres in scope
        genres = set()

        for inx, result in enumerate(ranked_results):
            if 'genres' in result:
                if type(result['genres']) != list:
                    result['genres'] = [str(x) for x in eval(result['genres'])]
                    ranked_results[inx]['genres'] = result['genres']

                for genre in list(result['genres']):
                    genres.add(genre)

        payload = {
            'genres': list(genres),
            'results': ranked_results,
            'feature_ranges': self.searchAlgConfig['feature_ranges'],
            'search_song_features': None
        }

        if songInfo:
            songInfo.update(choiceList)
            payload['search_song_features'] = songInfo

        return payload

    def format_result(self, result):

        #TODO figure out unicode for sharp and flat
        mode_map = [u"Minor", u"Major"]
        key_map = [u"C", u"C#/Db", u"D", u"D#/Eb", u"E", u"F", u"F#/Gb",
                   u"G", u"G/Ab", u"A", u"A/Bb", u"B"]

        formatted_result = result

        if 'tempo' in formatted_result:
            formatted_result['tempo'] = int(formatted_result['tempo'])
        if 'danceability' in formatted_result:
            formatted_result['danceability'] = int(formatted_result['danceability'] * 100)
        if 'energy' in formatted_result:
            formatted_result['energy'] = int(formatted_result['energy'] * 100)
        if 'speechiness' in formatted_result:
            formatted_result['speechiness'] = int(formatted_result['speechiness'] * 100)
        if 'acousticness' in formatted_result:
            formatted_result['acousticness'] = int(formatted_result['acousticness'] * 100)
        if 'instrumentalness' in formatted_result:
            formatted_result['instrumentalness'] = int(formatted_result['instrumentalness'] * 100)
        if 'liveness' in formatted_result:
            formatted_result['liveness'] = int(formatted_result['liveness'] * 100)
        if 'valence' in formatted_result:
            formatted_result['valence'] = int(formatted_result['valence'] * 100)
        if 'loudness' in formatted_result:
            formatted_result['loudness'] = int(formatted_result['loudness'])
        if 'duration_ms' in formatted_result:
            formatted_result['duration_ms'] = "{0}:{1}".format(int(formatted_result['duration_ms'] / 1000) / 60, str(int(formatted_result['duration_ms'] % 60)).zfill(2))
        if 'key' in formatted_result and 'mode' in formatted_result:
            formatted_result['key'] = "{0} {1}".format(key_map[int(formatted_result['key'])], mode_map[int(formatted_result['mode'])])

        return formatted_result

    # Set +/- ranges based on configuration file
    def setRanges(self, choiceList):

        minRange = {}
        maxRange = {}

        for attribute in choiceList.keys():
            minRange[attribute] = choiceList[attribute] - self.searchAlgConfig['plusMinus'][attribute]
            maxRange[attribute] = choiceList[attribute] + self.searchAlgConfig['plusMinus'][attribute]

        return minRange, maxRange

if __name__ == '__main__':

    # Testing

    # Test Audio Attributes only
    """
    input = {
        "tempo": 150,
        "key": 4,
        "time_signature": 4
    }
    """

    # Test song input
    search = sp_search.sp_search()
    song_results = search.track("here comes the sun")
    song_id = song_results['tracks']['items'][0]['id']
    attibutes = search.audio_features([song_id])[0]

    input = {
        "tempo": attibutes['tempo'],
        "key": attibutes['key'],
        "time_signature": attibutes['time_signature'],
        "acousticness": attibutes['acousticness'],
        "danceability": attibutes['danceability'],
        "energy": attibutes['energy'],
        "instrumentalness": attibutes['instrumentalness'],
        "liveness": attibutes['liveness'],
        "loudness": attibutes['loudness'],
        "mode": attibutes['mode'],
        "valence": attibutes['valence'],
        "speechiness": attibutes['speechiness'],
    }
    test = trackQuery(True)
    print(test.searchTracks(input, {"hi":"hi"}))
