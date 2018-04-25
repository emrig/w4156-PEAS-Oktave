# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'backend')))

import main
import unittest
import datetime
import json
from flask import jsonify
from backend import sp_search
import random

class MainTest(unittest.TestCase):
    """This class uses the Flask tests app to run an integration test against a
    local instance of the server."""

    def setUp(self):
        self.app = main.app.test_client()
        self.performance_time_seconds = 10.0
        self.search = sp_search.sp_search()

    def test_performance_attr_search(self):

        for i in range(0, 5):
            input = {
                "tempo": random.randint(60,201),
                "key": random.randint(0,11),
                "time_signature": random.randint(1,7)
                }
            self.push_assertTime(input, '/song_search_test_temp')



    def test_performance_track_search(self):

        songs = ["childish gambino redbone", "beatles here comes the sun", "nirvana smells like teen spirit",
                 "darude sandstorm", "george clinton atomic dog"]

        for song in songs:
            """
            song_results = self.search.track(song)
            song_id = song_results['tracks']['items'][0]['id']
            attibutes = self.search.audio_features([song_id])[0]

            input = {
                "tempo": attibutes['tempo'],
                "key": attibutes['key'],
                "time_signature": attibutes['time_signature'],
                "acousticness": attibutes['acousticness'],
                "danceability": attibutes['danceability'],
                "energy": attibutes['energy'],
                "instrumentalness": attibutes['instrumentalness'],
                "liveness": attibutes['liveness'],
                "loudness": attibutes['loudness'],
                "mode": attibutes['mode'],
                "valence": attibutes['valence'],
                "speechiness": attibutes['speechiness'],
            }
            """

            input = {
                "track_name": song
            }
            self.push_assertTime_tracksearch(input, '/track_search')



    def push_assertTime(self, input, route):

        start = datetime.datetime.now()
        rv = self.app.get(route, data=input)
        stop = datetime.datetime.now()
        execution_time = stop-start
        #print("Search of tempo={0}, key={1}, time={2} took {3} seconds with {4} results".format(input['tempo'], input['key'], input['time_signature'], execution_time, len(eval(rv.data)['data'])))
        self.assertGreater(self.performance_time_seconds, execution_time.seconds)

    def push_assertTime_tracksearch(self, input, route):

        start = datetime.datetime.now()
        rv1 = self.app.get(route, data=input)
        rv2 = self.app.get('/id_search', data={"track_id": json.loads(rv1.data)['data'][0]['id']})
        stop = datetime.datetime.now()
        execution_time = stop-start
        #print("Search of tempo={0}, key={1}, time={2} took {3} seconds with {4} results".format(input['tempo'], input['key'], input['time_signature'], execution_time, len(eval(rv.data)['data'])))
        self.assertGreater(self.performance_time_seconds*2, execution_time.seconds)

if __name__ == '__main__':
    unittest.main()
