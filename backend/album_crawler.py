"""
Author: Pankhuri Kumar
"""

import os
import sp_search
from datetime import datetime

# for reading artists - remove once added to DB
import pandas as pd
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
        # store all artists who weren't updated fully previous time/were never updated
        notUpdatedArtists = artistQueue[artistQueue["get_music_time"] <= lastUpdated]
        notUpdatedArtists = notUpdatedArtists.append(artistQueue[artistQueue["get_music_time"].isnull()])
        updatedArtists = []

        # store music for all these artists
        for artist in notUpdatedArtists.iterrows():
            albums = self.search.artist_albums(artist[1]["artist_id"])
            # compare with no. of albums in DB (csv)
            #TODO: figure how to keep track of albums when Spotify deletes album and adds another
            if (albums["total"] > artist[1]["albums"]):
                # find missing album(s)
                missingAlbums = self.findMissingAlbums(artist, albums)
                # update tracks to DB (csv) - track_crawler
                updateCount = self.updateTracks(missingAlbums)
                # update number of albums in DB (csv)
                artistQueue.ix[artistQueue["artist_id"] == artist[1]["artist_id"], ["albums"]] = artist[1]["albums"] + updateCount
            # keep track of all successfully traversed artists
            updatedArtists.append(artist[1]["artist_id"])

        # update artists_queue with get_music_time
        updateTime = datetime.now()
        for id in updatedArtists:
            artistQueue.ix[artistQueue["artist_id"] == id, ["get_music_time"]] = updateTime
        # write updates to DB (csv)
        artistQueue.to_csv(self.artistFile, index=False)

    def findMissingAlbums(self, artist, albums):
        missingAlbums = []

        #TODO: retrieve list of 'artist's album names from DB (csv)
        #TODO: handle if artist is new to DB (csv) - returns null existingAlbums
        existingAlbums = []
        for album in albums["items"]:
            if (album["name"] not in existingAlbums):
                missingAlbums.append(album["id"])

        return missingAlbums

    def updateTracks(self, missingAlbums):
        updateCount = 0

        #TODO: place in try-catch for API limit error - run by Album - Find the error that spotipy raises!
        # update track DB (csv)
        for album in missingAlbums:
            # query spotify using id
            tracks = self.search.album_tracks(album)
            # query for audio features
            for track in tracks["items"]:
                #TODO: write relevant from both data to DB (csv)
                trackId = track["id"]
                features = self.search.audio_features(trackId)
                # write to DB (csv) here - also write album name
            # increment only if entire album update is successful
            updateCount += 1

        return updateCount

if __name__ == "__main__":
    crawler = album_crawler()