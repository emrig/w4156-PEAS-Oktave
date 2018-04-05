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

from backend import trackQuery, environment
from firebase_admin import credentials
import firebase_admin
import unittest
import pandas as pd
import json
from flask import jsonify

class MainTest(unittest.TestCase):
    """This class uses the Flask tests app to run an integration test against a
    local instance of the server."""

    def setUp(self):
        envData = environment.Data()
        config = envData.config['pyrebaseConfig']
        localCredentials = credentials.Certificate(config['serviceAccount'])

        try:
            firebase_admin.initialize_app(localCredentials)
        except:
            None
        self.test_trackQuery = trackQuery.trackQuery(test=True)

    def test_hello_world(self):

        input = {

            "tempo": 100,
            "key": 4,
            "time_sig": 4
        }

        self.push_assertResult(100, 4, 4)

    def test_all_inputs(self):

        tempos = range(60,200)
        keys = range(0,12)
        time_sigs = range(1,8)
        no_result_list = []
        f = pd.read_csv("param_results2.csv")

        for tempo in tempos:
            for key in keys:
                for time_sig in time_sigs:
                    results = self.push_assertResult(tempo, key, time_sig)
                    f = f.append(pd.DataFrame([[tempo, key, time_sig, results]], columns=f.columns))
                    no_result_list.append((tempo, key, time_sig))
                    f.to_csv("param_results2.csv", index=False)

    def push_assertResult(self, tempo, key, time_sig):

        input = {
            "tempo_label": tempo,
            "key_label": key,
            "time_sig_label": time_sig
        }

        #print("Testing: tempo:{0} key:{1} time_sig:{2}".format(tempo, key, time_sig))
        results = self.test_trackQuery.searchTracks(input)

        self.assertGreater(len(results), -1)

        return len(results)

if __name__ == '__main__':
    unittest.main()
