"""
Author: Erin Riglin
"""

import os
import sp_search
import datetime
import environment
import json
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore
from google.cloud.exceptions import NotFound

"""
Useful documentation: 
https://firebase.google.com/docs/reference/admin/python/firebase_admin.db
https://github.com/thisbejim/Pyrebase
https://firebase.google.com/docs/database/security/indexing-data
"""

class artist_crawler:
    
    def __init__(self):

        env_data = environment.Data()

        self.crawler_config = env_data.config['crawlerConfig']
        self.init_artists = json.load(open(self.crawler_config['initArtists']))

        self.artist_config = env_data.config['databaseConfig']['artist_q']['artist_id']

        pyrebase_config = env_data.config['pyrebaseConfig']
        cred = credentials.Certificate(pyrebase_config['serviceAccount'])
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        self.config = env_data.config['crawlerConfig']
        self.search = sp_search.sp_search()

        self.rerun = False
        self.rerun_init_time = datetime.datetime.now()

    def initialize_artist_queue(self):

        for artist_id in self.init_artists.keys():

            add_artist(self.db, 'artist_q', self.init_artists[artist_id], self.artist_config).add()

    
    def pop_from_artist_queue(self):

        # Rerun the queue processor to add artists based on updated configuration
        if self.rerun:
            query = self.db.collection(u'artist_q').where(u'get_related_time', u'<', self.rerun_init_time).order_by(
                u'get_related_time', direction=firestore.Query.ASCENDING).limit(1000)

        else:
            query = self.db.collection(u'artist_q').where(u'get_related_time', u'==', 0).order_by(
                u'index', direction=firestore.Query.ASCENDING).limit(1000)

        artist_batch = []

        docs = query.get()

        # Process in bulk to save on number of requests made
        for doc in docs:
            artist_batch.append(doc.id)

        for artist_id in artist_batch:

            if self.push_related_artists(artist_id):
                ref = self.db.collection(u'artist_q').document(u'{0}'.format(artist_id))
                ref.update({u'get_related_time': datetime.datetime.now()})
                print("Update: {0} : {1}".format(artist_id, datetime.datetime.now()))
        
    
    def push_related_artists(self, artist_id):
        
        related_artists = self.search.artist_related_artist(artist_id)['artists']
        count = 0

        for artist in related_artists:

            # Add artist to queue if they do not already exist
            if add_artist(self.db, 'artist_q', artist, self.artist_config).add():
                count += 1

            if count == self.config['max_related_artists']:
                return True

        return True

    # Clean up function to add the name of every artist
    def set_artist_names(self):

        docs = self.db.collection(u'artist_q').get()
        artist_batch = []

        # Process in bulk to save on number of requests made
        for doc in docs:
            artist_batch.append(doc.id)

        count = 0

        for artist_id in artist_batch:

            artist = self.search.single_artist(artist_id)
            doc_ref = self.db.collection(u'artist_q').document(u'{0}'.format(artist_id))
            count += 1

            if artist:
                values = {

                    "name": artist['name'],
                    "popularity": artist['popularity']

                }
                result = doc_ref.update(values)
                print('{0}/{1} update: {2}'.format(count, len(artist_batch), values))
            else:
                print("{0} not found!".format(artist_id))


class add_artist(artist_crawler):

    def __init__(self, db, collection, artist, artist_config):

        env_data = environment.Data()
        self.crawler_config = env_data.config['crawlerConfig']
        self.db = db

        self.collection = collection
        self.artist = artist
        self.artist_id = artist['id']
        self.artist_config = artist_config
        self.artist_config['genres'] = artist['genres']
        self.artist_config['name'] = artist['name']
        self.artist_config['popularity'] = artist['popularity']

    def add(self):
        filtered_genres = [x for x in self.artist_config['genres'] if x in self.crawler_config['genres_ignore']]

        if self.artist['popularity'] < self.crawler_config['rating_minimum'] or filtered_genres:
            return False

        if not self.exists():
            self.artist_config['index'] = self.get_index()
            self.set()
            return True

        else:
            return False

    def get_index(self):
        query = self.db.collection(u'{0}'.format(self.collection)).order_by(
            u'index', direction=firestore.Query.DESCENDING).limit(1)

        docs = query.get()
        for doc in docs:
            val = doc.to_dict()
            if val['index'] < self.crawler_config['max_total_artists']:
                return val['index'] + 1
            else:
                raise NameError('Max Artist Size Reached')
        return 1

    def exists(self):
        doc_ref = self.db.collection(u'{0}'.format(self.collection)).document(u'{0}'.format(self.artist_id))

        try:
            doc = doc_ref.get()
            return True
        except NotFound:
            return False

    def set(self):
        doc_ref = self.db.collection(u'{0}'.format(self.collection)).document(u'{0}'.format(self.artist_id))
        doc_ref.set(self.artist_config)
        print('Set: {0}'.format(self.artist_config))

if __name__ == '__main__':


    test = artist_crawler()
    #test.initialize_artist_queue()

    test.set_artist_names()

    while(True):
        test.pop_from_artist_queue()
