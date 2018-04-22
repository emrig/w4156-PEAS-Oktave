from flask import Flask, render_template, request, jsonify
from backend import trackQuery
from backend import environment
from backend import sp_search
from firebase_admin import credentials
from firebase_admin import firestore
import  firebase_admin

app = Flask(__name__)

def start_firestore():

    # Disable app if happens to be enabled
    try:
        firebase_admin.delete_app(firebase_admin.get_app())
    except:
        pass

    try:
        firebase_admin.initialize_app()
    except:
        envData = environment.Data('dev')
        config = envData.config['pyrebaseConfig']
        localCredentials = credentials.Certificate(config['serviceAccount'])
        firebase_admin.initialize_app(localCredentials)

def stop_firestore():

    try:
        firebase_admin.delete_app(firebase_admin.get_app())
    except:
        pass

@app.route('/')
def homePage():
    return render_template('search.html')

@app.route('/about')
def about():
  return render_template("about.html")

# @app.route('/song_search', methods=['POST'])
# def search():
#     start_firestore()
#
#     input = {
#         "tempo": int(request.form['tempo']),
#         "key": int(request.form['key']),
#         "time_signature": int(request.form['time_sig'])
#     }
#
#     search = trackQuery.trackQuery()
#     results = search.searchTracks(input)
#
#     context = dict(data=results)
#
#     stop_firestore()
#
#     return render_template("track_search.html", **context)

@app.route('/attribute_search', methods=['GET'])
def search_test(input = None):
    start_firestore()

    if (input == None):
        input = {}
        for attribute in request.values.keys():
            input[attribute] = float(request.values[attribute])

    # TODO cleanup, ensure all incoming keys match the names in database

    if 'time_sig' in input:
        input['time_signature'] = input['time_sig']
        input.pop('time_sig', None)

    search = trackQuery.trackQuery()
    results = search.searchTracks(input)

    stop_firestore()

    return jsonify(data=results)

@app.route('/track_search', methods=['GET'])
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

    return jsonify(data=results)

@app.route('/id_search', methods=['GET'])
def search_for_id():
    track_id = request.values['track_uri']
    #TODO check format of ID

    search = sp_search.sp_search()
    results = search.track_by_id(track_id)



if __name__ == '__main__':
    app.run(debug=True)
