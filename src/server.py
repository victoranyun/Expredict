from flask import Flask, request, jsonify
import os
from util import file_upload
from creds import get_credentials, call_api
from get_long_lived_token import get_access_token

PATH = '../uploads'

ACCESS_RIGHTS = 0o755

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
    return '''
    <!doctype html>
    <html>
    <center>
    <title>Upload to Model</title>
    <h2>Upload File</h2>
    <form method=post enctype=multipart/form-data>
    <p><input type=file name=filename accept=image/* multiple>
    <input type=submit value=Upload>
    </form>
    </center>
    </html>
    '''


@app.route('/', methods=['POST'])
def run():
    file_path = file_upload(request, PATH)


@app.route('/auth/instagram', methods=['GET'])
def access():
    cred = get_credentials()
    res = get_access_token(cred)

    return jsonify(res['json_data']['access_token'])


@app.route('/instagram/<username>', methods=['GET'])
def get_data(username):
    cred = get_credentials()
    res = get_access_token(cred)

    return jsonify(res['json_data']['business_discovery'])


if __name__ == '__main__':
    if not os.path.exists(PATH):
        os.makedirs(PATH, ACCESS_RIGHTS)

    app.run(port=1337, host='127.0.0.1')
