from flask import Flask, request, jsonify
import os
from util import file_upload
from creds import get_credentials
from get_long_lived_token import get_access_token
from api import resize, run_prediction, find_max, display_image
from discovery_api import get_instagram_metadata
from get_id import get_facebook_pages
from flask_sqlalchemy import SQLAlchemy

PATH = '../uploads'

ACCESS_RIGHTS = 0o755

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://victory:victory@localhost:5432/expredict"
db = SQLAlchemy(app)

from models import Instagram


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
    parse_to_np = resize(file_path)
    result = run_prediction(parse_to_np)
    maximum_index = find_max(result)
    display_image(parse_to_np[maximum_index])
    return jsonify({'Expredicted': result.tolist()})


@app.route('/auth/instagram')
def access():
    cred = get_credentials()
    res = get_access_token(cred)
    access_token = res['json_data']
    # print(access_token['access_token'])
    try:
        account = Instagram(
            username='funmblr',
            access_token=access_token['access_token'],
            page_id='123',
            instagram_id='123'
        )
        db.session.add(account)
        db.session.commit()
        return jsonify(res['json_data'])
    except Exception as e:
        return str(e)


@app.route('/instagram/lookup/id', methods=['GET'])
def get_id():
    cred = get_credentials()
    res_for_id = get_facebook_pages(cred)
    ig_id = res_for_id['json_data']['instagram_business_account']['id']
    cred['ig_id'] = ig_id
    return ig_id


@app.route('/instagram/<username>', methods=['GET'])
def get_data(username):
    cred = get_credentials()
    res_for_id = get_facebook_pages(cred)
    ig_id = res_for_id['json_data']['instagram_business_account']['id']
    cred['ig_id'] = ig_id
    cred['username'] = username
    return jsonify(get_instagram_metadata(cred)['json_data']['business_discovery'])


if __name__ == '__main__':
    if not os.path.exists(PATH):
        os.makedirs(PATH, ACCESS_RIGHTS)

    app.run(ssl_context='adhoc', port='1337', debug=False)
