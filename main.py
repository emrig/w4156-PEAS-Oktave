from flask import Flask, render_template, request
from backend import artist_crawler as artistReference
from backend import album_crawler as trackReference

app = Flask(__name__)


# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='dummy_region',
#     aws_access_key_id='dummy_access_key',
#     aws_secret_access_key='dummy_secret_key',
#     verify=False)


@app.route('/')
def homePage():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
