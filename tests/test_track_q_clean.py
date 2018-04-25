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
from backend import album_crawler
from backend import track_q_clean
import random

class MainTest(unittest.TestCase):
    """This class uses the Flask tests app to run an integration test against a
    local instance of the server."""

    def setUp(self):
        self.app = main.app.test_client()
        self.performance_time_seconds = 10.0
        self.search = sp_search.sp_search()

    def test_performance_track_q_clean(self):

        self.push_assertTime(['artist_name', 'duration_ms', 'genres', 'album_art', 'preview_url'])


    def push_assertTime(self, attributes):

        test = track_q_clean.trackCleanup(test=True)
        self.assertTrue(test.add_track_attributes(attributes=attributes, test=True))


if __name__ == '__main__':
    unittest.main()
