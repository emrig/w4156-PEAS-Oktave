"""
Author: Pankhuri Kumar
"""

import sp_search
import environment
from datetime import datetime
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
        self.market = envData.config['crawlerConfig']['markets']

        self.read_input()

    def read_input(self):

        lastUpdatedTime = ''
        lastUpdated = self.artistReference.order_by(u'get_music_time', direction=firestore.Query.DESCENDING).limit(1).get()
        for a in lastUpdated:
            lastUpdatedTime = (a.to_dict())["get_music_time"]

        # update artists_queue with get_music_time and new album count
        self.updateTime = datetime.now()

        # store all artists who were never updated and store music for all these artists
        found = 1
        found1 = 0
        while found != 0:
            try:
                nullArtist = self.artistReference.where(u'get_music_time', u'==', 0).order_by(u'index').limit(20).get()
                for i in range(0, 20):
                    self.findTracks(nullArtist[i], lastUpdatedTime)
                found += 1
            except NotFound:
                found1 = found
                found = 0
                pass
        # store all artists who weren't updated fully previous time and store music for all these artists
        found = found1
        internalIndex = 1
        while found != 0:
            try:
                notUpdatedArtist = self.artistReference.where(u'index', u'==', internalIndex).get()
                self.findTracks(notUpdatedArtist, lastUpdatedTime)
                internalIndex += 1
                found += 1
            except NotFound:
                print("Successfully updated " + str(found) + " artists' information!")
                print("...Exiting Now...")
                found = 0
                pass

    def findTracks(self, toBeUpdated, lastUpdatedTime):

        for item in toBeUpdated:
            artist = item.to_dict()

            # to handle change in date format
            try:
                # if artist was updated in last pass, assumes application was interrupted for some reason
                if artist['get_music_time'] == lastUpdatedTime:
                    continue
            except TypeError:
                pass

            albums = self.search.artist_albums(item.id)
            #TODO: figure how to keep track of albums when Spotify deletes album and adds another
            if (albums["total"] > artist["albums"]):
                # find missing album(s)
                missingAlbums = self.findMissingAlbums(item.id, albums)
                updateCount = self.updateTracks(item.id, missingAlbums)
                # update number of albums
                artist["albums"] += updateCount
                artist["get_music_time"] = self.updateTime
            # write updates to DB (csv)
            self.artistReference.document(item.id).update(artist)

    def findMissingAlbums(self, artist, albums):
        missingAlbums = []

        # retrieve list of 'artist's album names from DB (csv)
        existingAlbums = []
        found = 1
        while found != 0:
            # if artist is new to DB
            try:
                existsInDB = self.trackReference.where(u'artist_id', u'==', artist).limit(1).get()
                for item in existsInDB:
                    existingAlbums.append(item.id)
            except NotFound:
                found = 0
                pass

        # check if album already in DB, and in defined markets
        for album in albums["items"]:
            if (album["id"] not in existingAlbums) and set(self.market).issubset(set(album['available_markets'])):
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
                # fill up entry with relevant information
                entry = self.initializeEntry(track)
                entry["artist_id"] = artist
                entry["album_id"] = album

                # add song to DB if it doesn't exist
                if (not self.exists(track['id'])):
                    print(".... .... adding " + str(track['id']))
                    self.trackReference.document(track['id']).set(entry)
                # else update song info
                else:
                    print(".... .... updating " + str(track['id']))
                    self.trackReference.document(track['id']).update(entry)

            # increment only if entire album update is successful
            updateCount += 1

        return updateCount

    def initializeEntry(self, track):
        trackId = track["id"]

        entry = self.trackConfig
        entry["name"] = track['name']
        features = self.search.audio_features(str(trackId))

        # when some features don't exist in Spotify DB
        try: entry["danceability"] = features[0]["danceability"]
        except: pass
        try: entry["energy"] = features[0]["energy"]
        except: pass
        try: entry["key"] = features[0]["key"]
        except: pass
        try: entry["loudness"] = features[0]["loudness"]
        except: pass
        try: entry["mode"] = features[0]["mode"]
        except: pass
        try: entry["speechiness"] = features[0]["speechiness"]
        except: pass
        try: entry["acousticness"] = features[0]["acousticness"]
        except: pass
        try: entry["instrumentalness"] = features[0]["instrumentalness"]
        except: pass
        try: entry["liveness"] = features[0]["liveness"]
        except: pass
        try: entry["valence"] = features[0]["valence"]
        except: pass
        try: entry["tempo"] = features[0]["tempo"]
        except: pass
        try: entry["time_signature"] = features[0]["time_signature"]
        except: pass
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