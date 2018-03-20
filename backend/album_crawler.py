"""
Author: Pankhuri Kumar
"""

import pyrebase
import sp_search
import environment
from datetime import datetime

class album_crawler():

    def __init__(self):

        envData = environment.Data()

        pyrebaseConfig = envData.config['pyrebaseConfig']
        self.firebase = pyrebase.initialize_app(pyrebaseConfig)
        self.database = self.firebase.database()

        self.trackConfig = envData.config['databaseConfig']['track_features']['track_q']['track_id']

        self.search = sp_search.sp_search()

        self.read_input()

    def read_input(self):

        lastUpdatedTime = ""
        lastUpdated = self.database.child("crawlerTable").child("artist_q").order_by_child("get_music_time").limit_to_last(1).get().val()
        for a in lastUpdated:
            lastUpdatedTime = lastUpdated[a]["get_music_time"]

        # find max datetime in get_music_time
        # store all artists who weren't updated fully previous time/were never updated
        # and store music for all these artists
        nullArtists = self.database.child("crawlerTable").child("artist_q").order_by_child("get_music_time").equal_to("").get()
        self.findTracks(nullArtists)
        if lastUpdatedTime != '':
            notUpdatedArtists = self.database.child("crawlerTable").child("artist_q").order_by_child("get_music_time").start_at(lastUpdatedTime).get()
            self.findTracks(notUpdatedArtists)

    def findTracks(self, toBeUpdated):

        updatedArtists = []

        for item in toBeUpdated.each():
            albums = self.search.artist_albums(item.key())
            artist = item.val()
            #TODO: figure how to keep track of albums when Spotify deletes album and adds another
            if (albums["total"] > artist["albums"]):
                # find missing album(s)
                missingAlbums = self.findMissingAlbums(item.key(), albums)
                updateCount = self.updateTracks(item.key(), missingAlbums)
                # update number of albums
                artist["albums"] = albums["total"] + updateCount
            # keep track of all successfully traversed artists
            updatedArtists.append(item.key())

        # update artists_queue with get_music_time and new album count
        updateTime = datetime.now()
        for item in toBeUpdated.each():
            artist = item.val()
            if item.key() in updatedArtists:
                artist["get_music_time"] = updateTime
                # write updates to DB (csv)
                self.database.child("crawlerTable").child("artist_q").update({item.key(): artist})

    def findMissingAlbums(self, artist, albums):
        missingAlbums = []

        # retrieve list of 'artist's album names from DB (csv)
        #TODO: handle if artist is new to DB (csv) - returns null existingAlbums
        # existsInDB = self.database.child("track_features").child("track_q").order_by_child("artist_id").equal_to(artist).get()
        # existingAlbums = existsInDB.val()

        for album in albums["items"]:
            #TODO: remove below comment after initial DB population
            # if (album["id"] not in existingAlbums):
            missingAlbums.append(album["id"])

        return missingAlbums

    def updateTracks(self, artist, missingAlbums):
        updateCount = 0

        #TODO: place in try-catch for API limit error - run by Album - Find the error that spotipy raises!
        # update track DB (csv)
        for album in missingAlbums:
            # query spotify using id
            tracks = self.search.album_tracks(album)
            # query for audio features
            for track in tracks["items"]:
                # write relevant data to DB (csv)
                entry = self.initializeEntry(track)
                entry["artist_id"] = artist
                entry["album_id"] = album["id"]
                self.database.child('track_features').child('track_q').update({track["id"]: entry})
            # increment only if entire album update is successful
            updateCount += 1

        return updateCount

    def initializeEntry(self, track):
        trackId = track["id"]
        features = self.search.audio_features(trackId)

        entry = self.trackConfig
        entry["name"] = track['name']
        entry["danceability"] = features["danceability"]
        entry["key"] = features["key"]
        entry["valence"] = features["valence"]
        entry["tempo"] = features["tempo"]
        entry["time_signature"] = features["time_signature"]

        return entry

if __name__ == "__main__":
    crawler = album_crawler()