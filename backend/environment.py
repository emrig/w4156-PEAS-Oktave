import os
import json

class Data():

    def __init__(self):
        self.env = 'dev'

        self.config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "configuration", "app.json"))
        self.config = eval(open(self.config_file, 'r').read())[self.env]

        self.config['pyrebaseConfig']["serviceAccount"] = os.path.abspath(os.path.join(os.path.pardir, self.config['pyrebaseConfig']["serviceAccount"]))
        self.config['crawlerConfig']["initArtists"] = os.path.abspath(os.path.join(os.path.pardir, self.config['crawlerConfig']["initArtists"]))
