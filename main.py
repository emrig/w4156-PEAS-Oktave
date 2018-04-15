flag = 5
flag2 = 3

from flask import Flask, render_template, request, jsonify
from backend import trackQuery
from backend import environment
from backend import sp_search
from firebase_admin import credentials
import  firebase_admin

app = Flask(__name__)


# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='dummy_region',
#     aws_access_key_id='dummy_access_key',
#     aws_secret_access_key='dummy_secret_key',
#     verify=False)

# Initialize Firebase Admin
envData = environment.Data()
config = envData.config['pyrebaseConfig']
localCredentials = credentials.Certificate(config['serviceAccount'])
firebase_admin.initialize_app(localCredentials)


@app.route('/')
def homePage():
    return render_template('search.html')

@app.route('/song_search', methods=['POST'])
def search():

    input = {
        "tempo": int(request.form['tempo']),
        "key": int(request.form['key']),
        "time_signature": int(request.form['time_sig'])
    }

    search = trackQuery.trackQuery()
    results = search.searchTracks(input)

    context = dict(data=results)

    return render_template("track_search.html", **context)

@app.route('/song_search_test_temp', methods=['GET'])
def search_test():

    input = {}

    for attribute in request.values.keys():
        input[attribute] = float(request.values[attribute])

    # TODO cleanup, ensure all incoming keys match the names in database

    if 'time_sig' in input:
        input['time_signature'] = input['time_sig']
        input.pop('time_sig', None)

    search = trackQuery.trackQuery()
    results = search.searchTracks(input)

    #context = dict(data=results)

    return jsonify(data=results)

@app.route('/search_by_track', methods=['GET'])
def search_by_track():

    input = {
        "track_name": request.values['track_name']
    }

    search = sp_search.sp_search()
    results_raw = search.track(input['track_name'])

    results = []

    for track in results_raw['tracks']['items']:

        json = {}
        json['name'] = track['name']
        json['artist_name'] = track['artists'][0]['name']
        json['album_name'] = track['album']['name']
        json['id'] = track['id']
        json['album_id'] = track['album']['id']
        json['album_art'] = track['album']['images'][0]['url']
        json['artist_id'] = track['artists'][0]['id']
        json['preview_url'] = track['preview_url']
        json['duration_ms'] = track['duration_ms']
        json['uri'] = track['uri']

        results.append(json)

    #context = dict(data=results)

    return jsonify(data=results)

if __name__ == '__main__':
    app.run(debug=True)
