"""
Author: Erin Riglin
"""

import os
import sp_search
import datetime
import environment
import pyrebase
import json

"""Remove after initial dev with csv"""
import pandas as pd

"""
Useful documentation: 
https://firebase.google.com/docs/reference/admin/python/firebase_admin.db
https://github.com/thisbejim/Pyrebase
https://firebase.google.com/docs/database/security/indexing-data
"""

class artist_crawler():
    
    def __init__(self):

        env_data = environment.Data()

        self.crawler_config = env_data.config['crawlerConfig']
        self.init_artists = json.load(open(self.crawler_config['initArtists']))

        self.artist_config = env_data.config['databaseConfig']['crawlerTable']['artist_q']['artist_id']

        pyrebase_config = env_data.config['pyrebaseConfig']
        self.firebase = pyrebase.initialize_app(pyrebase_config)
        self.db = self.firebase.database()

        self.config = env_data.config['crawlerConfig']
        self.search = sp_search.sp_search()
        
        # remove after initial csv dev
        self.queue_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "artist_queue.csv"))
        
        self.initialized_artists = self.initialize_artist_queue()
        
    """ For initial csv and file output only. Modify or remove for cloud DB """

    def initialize_artist_queue(self):

        for artist_id in self.init_artists.keys():

            entry = self.artist_config
            last = self.db.child('crawlerTable').child('artist_q').order_by_child('index').limit_to_last(1).get()

            """ If table empty and if artist already exists in table"""
            if not last.pyres:
                entry['index'] = 1
                entry['genres'] = self.init_artists[artist_id]['genres']
                self.db.child('crawlerTable').child('artist_q').update({artist_id: entry})

            elif not self.db.child('crawlerTable').child('artist_q').child(artist_id).get().pyres:
                last_index = last.val().popitem()[1]['index']
                if last_index < self.crawler_config['max_total_artists']:
                    entry['index'] = last.val().popitem()[1]['index'] + 1
                    entry['genres'] = self.init_artists[artist_id]['genres']
                    self.db.child('crawlerTable').child('artist_q').update({artist_id: entry})

    
    def pop_from_artist_queue(self):
        
        df = pd.read_csv(self.queue_file)
        stack = df[df['get_related_time'].isnull()]
        top_index = stack['index'].idxmin()
        artist_id = stack.loc[top_index]['artist_id']
        df = self.push_related_artists(artist_id, df)
        
        new_index = df.index[df['artist_id'] == artist_id].tolist()
        if len(new_index) > 1:
            #Throw Error
            print("Duplicate Error: indices " + new_index)
        else:
            new_index = new_index[0]
            df.at[new_index, 'get_related_time'] = datetime.datetime.now()
            df.to_csv(self.queue_file, index=False)
                
        
    
    def push_related_artists(self, artist_id, df):
        
        related_artists = self.search.artist_related_artist(artist_id)['artists']
        
        for artist in related_artists:
            
            filtered_genres = [x for x in artist['genres'] if x in self.config['genres_ignore']]
            
            # Check config filter rules
            if filtered_genres or artist['popularity'] < self.config['rating_minimum']:
                break
            
            """ Modify for DB HTTP calls """
            # Do not include artists already in DB
            if len(df['artist_id']) < self.config['max_total_artists'] and artist['id'] not in list(df['artist_id']):
            
                if df['index'].empty:
                    index = 1
                else:
                    index = max(df['index']) + 1
                    
                df = df.append(pd.DataFrame([[artist['id'], index, None, None, artist['genres']]], columns=df.columns))
        
        df = df.reset_index(drop=True)
        return df
        
        # """try:
        #     Note atomic consideration here for updating parent artist
        #     df.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "artist_queue.csv")), index=False)
        #     return True
        #
        # except Exception as e:
        #     print("[log]: " + str(e))
        #     return False
        #     """
      
    
        
if __name__ == '__main__':


    test = artist_crawler()
    #test.initialize_artist_queue()
    #print(test.config)

    #while (pd.read_csv(test.queue_file)['artist_id'].size < test.config['max_total_artists']):

     #   test.pop_from_artist_queue()
