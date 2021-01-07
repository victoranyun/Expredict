from flask import Flask, request, jsonify
import os
from util import file_upload
from creds import get_credentials, call_api
from get_long_lived_token import get_access_token
from api import resize, run_prediction, find_max, display_image
from get_id import get_facebook_pages
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

PATH = '../uploads'

ACCESS_RIGHTS = 0o755

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://victory:victory@localhost:5432/expredict"
db = SQLAlchemy(app)

from models import Instagram


@app.route('/', methods=['GET'])
def index_page(name=None):
    """
    Index page for uploading a bunch of pictures
    :return: the view of the page
    """
    return render_template("index.html", name=name)


@app.route('/', methods=['POST'])
def run():
    """
    Prints Expredicted array of predictions from the model
    :return: view
    """
    file_path = file_upload(request, PATH)
    parse_to_np = resize(file_path)
    result = run_prediction(parse_to_np)
    maximum_index = find_max(result)
    display_image(parse_to_np[maximum_index])
    return jsonify({'Expredicted': result.tolist()})


@app.route('/auth/instagram')
def access():
    """
    Using the basic credentials, stores in PostgreSQL, gets useful data and "authenticates"
    :return: access token + bearer
    """
    cred = get_credentials()
    res = get_access_token(cred)
    access_token = res['json_data']

    res_for_id = get_facebook_pages(cred)
    ig_id = res_for_id[1]['json_data']['instagram_business_account']['id']
    account_username = res_for_id[0]

    try:
        account = Instagram(
            username=account_username,
            access_token=access_token['access_token'],
            instagram_id=ig_id
        )
        db.session.add(account)
        db.session.commit()
        return jsonify(res['json_data'])
    except Exception as e:
        return str(e)


@app.route('/instagram/lookup/<user_id>', methods=['GET'])
def get_info(user_id):
    """
    Perform query of lookup by primary id
    :param user_id: primary id
    :return: username, access_token, and instagram_id of said id
    """
    try:
        account = Instagram.query.get_or_404(user_id)
        response = {
            "username": account.username,
            "access_token": account.access_token,
            "instagram_id": account.instagram_id
        }
        return "username: " + response['username'] + " access_token: " + response['access_token'] + " instagram_id: " + \
               response['instagram_id']
    except Exception as e:
        return str(e)


@app.route('/instagram/<username>', methods=['GET'])
def get_data(username):
    """
    Queries any business/creator account using Instagram's new API and shows their metadata
    :param username: the username to query
    :return: the info: username,name,profile_picture_url,biography,follows_count,followers_count,media_count
    """
    parameters = dict()
    account = Instagram.query.first()
    parameters['access_token'] = account.access_token
    url = "https://graph.facebook.com/" + account.instagram_id + '?fields=business_discovery.username(' + \
          username + '){username,name,profile_picture_url,biography,follows_count,followers_count,media_count}'
    response = call_api(url, parameters)
    return jsonify(response['json_data']['business_discovery'])


if __name__ == '__main__':
    if not os.path.exists(PATH):
        os.makedirs(PATH, ACCESS_RIGHTS)

    app.run(ssl_context='adhoc', port='5000', debug=False)

