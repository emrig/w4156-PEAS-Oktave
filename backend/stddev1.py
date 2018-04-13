import sp_search
import environment
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore
from google.cloud.exceptions import NotFound
import numpy

envData = environment.Data()

pyrebaseConfig = envData.config['pyrebaseConfig']
localCredentials = credentials.Certificate(pyrebaseConfig['serviceAccount'])
firebase_admin.initialize_app(localCredentials)

database = firestore.client()
artistReference = database.collection(u'artist_q')
trackReference = database.collection(u'track_q')

myFile = open('musicDetails.txt', 'w')

docs = trackReference.get()

for doc in docs:
    myFile.write(u'{}'.format(doc.to_dict()))
    myFile.write('\n')

myFile.close()