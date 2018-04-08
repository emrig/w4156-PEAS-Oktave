from flask import Flask, render_template, request, jsonify
from backend import trackQuery
from backend import environment
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
        "tempo_label": int(request.form['tempo']),
        "key_label": int(request.form['key']),
        "time_sig_label": int(request.form['time_sig'])
    }

    search = trackQuery.trackQuery()
    results = search.searchTracks(input)

    context = dict(data=results)

    return render_template("track_search.html", **context)

@app.route('/song_search_test_temp', methods=['GET'])
def search_test():

    input = {
        "tempo_label": int(request.form['tempo']),
        "key_label": int(request.form['key']),
        "time_sig_label": int(request.form['time_sig'])
    }

    search = trackQuery.trackQuery()
    results = search.searchTracks(input)

    context = dict(data=results)

    return jsonify(data=results)

if __name__ == '__main__':
    app.run(debug=True)
