from flask import Flask
import os

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
    <p><input type=file name=file accept=image/* multiple>
    <input type=submit value=Upload>
    </form>
    </center>
    </html>
    '''


if __name__ == '__main__':
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    app.run(port=1337, host='127.0.0.1')
