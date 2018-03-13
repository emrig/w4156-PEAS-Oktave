import os
import sp_search
from datetime import datetime

# for reading artists - remove once added to DB
import pandas as pd
import csv
# for easy display of API while developing
import json

class album_crawler():

    def __init__(self):

        config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "configuration_test.json"))
        self.config = json.loads(open(config_file, 'r').read())
        self.search = sp_search.sp_search()

        self.artistFile = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "artist_queue.csv"))
        self.read_input()


    def read_input(self):

        artistQueue = pd.read_csv(self.artistFile)

        # find max datetime in get_music_time
        lastUpdated = artistQueue["get_music_time"].max()
        # store all artists who weren't updated last time/were never updated
        notUpdatedArtists = artistQueue[artistQueue["get_music_time"] < lastUpdated]
        notUpdatedArtists = notUpdatedArtists.append(artistQueue[artistQueue["get_music_time"].isnull()])
        updatedArtists = []

        # store music for all these artists
        #TODO place in try-catch for API limit error
        for artist in notUpdatedArtists.iterrows():
            albums = self.search.artist_albums(artist[1]["artist_id"])

            # compare with no. of albums in DB (csv)
            if (albums["total"] > artist[1]["albums"]):
                #TODO if unequal, update track dataframe
                # find missing album(s)
                # update tracks to DB (csv) - track_crawler
                # update number of albums in DB (csv)
                artistQueue.ix[artistQueue["artist_id"] == artist[1]["artist_id"], ["albums"]] = albums["total"]
                # print(artist[1]["artist_id"])

            # keep track of all successfully traversed artists
            updatedArtists.append(artist[1]["artist_id"])

        # update artists_queue with get_music_time
        updateTime = datetime.now()
        for id in updatedArtists:
            artistQueue.ix[artistQueue["artist_id"] == id, ["get_music_time"]] = updateTime

        # write updates to DB (csv)
        artistQueue.to_csv(self.artistFile, index=False)

if __name__ == "__main__":
    crawler = album_crawler()