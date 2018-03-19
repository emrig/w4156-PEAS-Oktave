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

        self.search = sp_search.sp_search()

        self.read_input()

    def read_input(self):

        lastUpdatedTime = ""
        lastUpdated = self.database.child("crawlerTable").child("artist_q").order_by_child("get_music_time").limit_to_last(1).get().val()
        for a in lastUpdated:
            lastUpdatedTime = lastUpdated[a]["get_music_time"]

        # find max datetime in get_music_time
        # store all artists who weren't updated fully previous time/were never updated
        nullArtists = self.database.child("crawlerTable").child("artist_q").order_by_child("get_music_time").equal_to("").get()
        if lastUpdated.pyres:
            notUpdatedArtists = self.database.child("crawlerTable").child("artist_q").order_by_child("get_music_time").start_at(lastUpdatedTime).get()

        # store music for all these artists
        self.findTracks(nullArtists)
        self.findTracks(notUpdatedArtists)

    def findTracks(self, toBeUpdated):

        updatedArtists = []

        for item in toBeUpdated.each():
            albums = self.search.artist_albums(item.key())
            artist = item.val()
            #TODO: figure how to keep track of albums when Spotify deletes album and adds another
            if (albums["total"] > artist["albums"]):
                # find missing album(s)
                missingAlbums = self.findMissingAlbums(artist, albums)
                updateCount = self.updateTracks(missingAlbums)
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