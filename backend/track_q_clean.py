"""
Author: Erin Riglin
"""

import environment
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.exceptions import NotFound
import sp_search
import datetime

class trackCleanup:

    def __init__(self, test=False, verbose=False):
        envData = environment.Data()

        config = envData.config['pyrebaseConfig']
        self.test = test
        self.verbose = verbose
        self.script_starttime = datetime.datetime.now()


        if self.test:
            localCredentials = credentials.Certificate(config['serviceAccount'])
            try:
                firebase_admin.initialize_app(localCredentials)
            except:
                None

        self.db = firestore.client()
        self.searchAlgConfig = envData.config['searchAlg']

        self.database = firestore.client()
        self.artistReference = self.database.collection(u'artist_q')
        self.trackReference = self.database.collection(u'track_q')

        self.search = sp_search.sp_search()


    def add_track_attributes(self, attributes=['artist_name'], test=False):

        energy = 0
        results = {}
        artists = {}

        if 'genres' in attributes:
            query = self.artistReference
            docs = query.get()
            for doc in docs:
                artists[doc.id] = doc.to_dict()

        while(True):

            query = self.trackReference.where(u'energy', u'>=', energy).order_by(
                u'energy', direction=firestore.Query.ASCENDING).limit(10000)

            try:
                docs = query.get()
            except NotFound:
                break

            for doc in docs:
                result = doc.to_dict()
                missing_attributes = []
                for attribute in attributes:
                    if attribute not in result:
                        results[doc.id] = doc.to_dict()

            energy = result['energy']
            print(len(results.keys()))

            batch = self.db.batch()

            for inx, result in enumerate(results.keys()):

                search_result = self.search.track_by_id(result)

                values = {}

                if 'artist_name' in attributes and 'artist_name' not in results[result]:
                    values['artist_name'] = search_result['artists'][0]['name']

                if 'duration_ms' in attributes and 'duration_ms' not in results[result]:
                    values['duration_ms'] = search_result['duration_ms']

                if 'genres' in attributes and 'genres' not in results[result]:
                    #album_result = self.search.album(results[result]['album_id'])
                    if 'artist_id' in results[result]:
                        values['genres'] = artists[results[result]['artist_id']]['genres']

                if 'album_art' in attributes and 'album_art' not in results[result]:
                    album_search_result = self.search.album(results[result]['album_id'])
                    values['album_art'] = album_search_result['images'][0]['url']

                if 'preview_url' in attributes and 'preview_url' not in results[result]:
                    values['preview_url'] = search_result['preview_url']

                #print(results[result]['name'] + ": " + str(values))
                doc_ref = self.db.collection(u'track_q').document(u'{0}'.format(result))
                batch.update(doc_ref, values)
                #print(len(batch._write_pbs))

                if len(batch._write_pbs) == 499 or inx == len(results.keys())-1:
                    batch.commit()
                    print("Commit!")
                    batch = self.db.batch()

            results = {}

            if (test):
                return True

        return

    def extract_artist_q(self):
        artists = {}
        query = self.artistReference
        docs = query.get()
        f = open('artist_q_backup.json', 'w')
        for doc in docs:
            artists[doc.id] = doc.to_dict()


        f.write(str(artists))
        f.close()

    def extract_track_q(self):
        tracks = {}
        energy = 0
        length = 0

        while (True):
            query = self.trackReference.where(u'energy', u'>=', energy).order_by(
                u'energy', direction=firestore.Query.ASCENDING).limit(20000)

            try:
                docs = query.get()
            except NotFound:
                return "done!"

            for doc in docs:
                tracks[doc.id] = doc.to_dict()
                result = doc.to_dict()

            energy = result['energy']
            print(len(tracks.keys()))

            if len(tracks.keys()) > length:
                length = len(tracks.keys())
            else:
                break

        f = open('track_q_backup.json', 'w')


        f.write(str(tracks))
        f.close()

if __name__ == '__main__':

    test = trackCleanup(test=True)
    test.add_track_attributes(attributes=['preview_url'])
    #test.extract_artist_q()
    #print(test.extract_track_q())
