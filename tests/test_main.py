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

class MainTest(unittest.TestCase):
    """This class uses the Flask tests app to run an integration test against a
    local instance of the server."""

    def setUp(self):
        self.app = main.app.test_client()
        self.performance_time_seconds = 5


    def test_performance(self):

        self.push_assertTime(100, 4, 4)

    def push_assertTime(self, tempo, key, time_sig):

        input = {
            "tempo": tempo,
            "key": key,
            "time_sig": time_sig
        }

        start = datetime.datetime.now()
        rv = self.app.get('/song_search_test_temp', data=input)
        stop = datetime.datetime.now()
        execution_time = stop-start
        self.assertGreater(self.performance_time_seconds, execution_time.seconds)

if __name__ == '__main__':
    unittest.main()
