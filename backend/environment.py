import os
import json
from definitions import ROOT_DIR

class Data():

    def __init__(self):
        self.env = 'dev'

        self.config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "configuration", "app.json"))
        self.config = eval(open(self.config_file, 'r').read())[self.env]

        self.config['crawlerConfig']["initArtists"] = os.path.abspath(os.path.join(os.path.pardir, self.config['crawlerConfig']["initArtists"]))
        self.config['pyrebaseConfig']["serviceAccount"] = os.path.abspath(os.path.join(ROOT_DIR, self.config['pyrebaseConfig']["serviceAccount"]))

if __name__ == "__main__":

    test = Data()
    print(test.config["pyrebaseConfig"]["serviceAccount"])
