"""
Author: Pankhuri Kumar
"""

import sp_search
import environment
from datetime import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.exceptions import NotFound

class album_crawler():

    def __init__(self):

        envData = environment.Data()

        pyrebaseConfig = envData.config['pyrebaseConfig']
        localCredentials = credentials.Certificate(pyrebaseConfig['serviceAccount'])
        firebase_admin.initialize_app(localCredentials)
        self.database = firestore.client()
        self.artistReference = self.database.collection(u'artist_q')
        self.trackReference = self.database.collection(u'track_q')

        self.trackConfig = envData.config['databaseConfig']['track_q']['track_id']
        self.search = sp_search.sp_search()

        self.read_input()

    def read_input(self):

        lastUpdatedTime = ''
        lastUpdated = self.artistReference.order_by(u'get_music_time', direction=firestore.Query.DESCENDING).limit(1).get()
        for a in lastUpdated:
            lastUpdatedTime = (a.to_dict())["get_music_time"]

        # update artists_queue with get_music_time and new album count
        s = datetime.now()
        self.updateTime = time.mktime(s.timetuple())

        # find max datetime in get_music_time
        # store all artists who weren't updated fully previous time/were never updated
        # and store music for all these artists
        found = 1
        while found != 0:
            try:
                nullArtist = self.artistReference.where(u'get_music_time', u'==', 0).order_by(u'index').limit(1).get()
                self.findTracks(nullArtist)
                print(found)
                found += 1
            except NotFound:
                found = 0
                pass

        if lastUpdatedTime != 0:
            found1 = 1
            while found1 != 0:
                try:
                    notUpdatedArtist = self.artistReference.where(u'get_music_time', u'<', lastUpdatedTime).order_by(u'index').limit(1).get()
                    self.findTracks(notUpdatedArtist)
                    print(found1)
                    found1 += 1
                except NotFound:
                    found1  = 0
                    pass

    def findTracks(self, toBeUpdated):

        for item in toBeUpdated:
            print("Starting Artist: " + str(item.id))
            albums = self.search.artist_albums(item.id)
            artist = item.to_dict()
            #TODO: figure how to keep track of albums when Spotify deletes album and adds another
            if (albums["total"] > artist["albums"]):
                # find missing album(s)
                missingAlbums = self.findMissingAlbums(item.id, albums)
                updateCount = self.updateTracks(item.id, missingAlbums)
                # update number of albums
                artist["albums"] = albums["total"] + updateCount
                artist["get_music_time"] = self.updateTime
                # write updates to DB (csv)
                self.artistReference.document(item.id).update(artist)
                print("Done with " + str(item.id))

    def findMissingAlbums(self, artist, albums):
        missingAlbums = []

        # retrieve list of 'artist's album names from DB (csv)
        #TODO: handle if artist is new to DB (csv) - returns null existingAlbums
        # existsInDB = self.trackReference.where(u'artist_id', u'==', artist).get()
        # existingAlbums = []
        # for e in existsInDB:
        #     existingAlbums.append(e.id)

        for album in albums["items"]:
            #TODO: remove below comment after initial DB population
            # if (album["id"] not in existingAlbums):
            missingAlbums.append(album["id"])
            if len(missingAlbums) > 5:
                break

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
                entry["album_id"] = album
                if not self.exists(track['id']):
                    self.trackReference.document(track['id']).set(entry)
            # increment only if entire album update is successful
            updateCount += 1
            print("Updated " + str(album))

        return updateCount

    def initializeEntry(self, track):
        trackId = track["id"]
        # print(features[0])

        entry = self.trackConfig
        entry["name"] = track['name']
        try:
            features = self.search.audio_features(str(trackId))
            entry["danceability"] = features[0]["danceability"]
            entry["key"] = features[0]["key"]
            entry["valence"] = features[0]["valence"]
            entry["tempo"] = features[0]["tempo"]
            entry["time_signature"] = features[0]["time_signature"]
        except:
            pass
        return entry

    def exists(self, trackID):
        trackRef = self.trackReference.document(trackID)

        try:
            doc = trackRef.get()
            return True
        except NotFound:
            return False

if __name__ == "__main__":
    crawler = album_crawler()