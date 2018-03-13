import os
import json
import sp_search
import datetime

"""Remove after initial dev with csv"""
import pandas as pd

class artist_crawler():
    
    def __init__(self):

        config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "configuration_test.json"))
        self.config = json.loads(open(config_file, 'r').read())
        self.search = sp_search.sp_search()
        
        # remove after inital csv dev
        self.queue_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "artist_queue.csv"))
        
        self.initialized_artists = self.initialize_artist_queue()
        
    """ For initial csv and file output only. Modify or remove for cloud DB """
    def initialize_artist_queue(self):
        
        loaded_artists = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "artists.csv")))
        df = pd.read_csv(self.queue_file)
        
        for artist in loaded_artists.iterrows():
            if artist[1]['id'] not in list(df['artist_id']):
                df = df.append(pd.DataFrame([[artist[1]['id'], df['index'].argmax()+1, None, None, artist[1]['genres']]], columns=df.columns))
                df = df.reset_index(drop=True)
                df.to_csv(self.queue_file, index=False)
    
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
    while (pd.read_csv(test.queue_file)['artist_id'].size < test.config['max_total_artists']):

        test.pop_from_artist_queue()