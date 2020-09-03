from flask import Flask
import os

PATH = '../uploads'

access_rights = 0o755
try:
    os.mkdir(PATH, access_rights)
except OSError:
    print("Failed to create directory %s due to duplicate dir or permissions" % PATH)
else:
    print("Successfully created the directory %s" % PATH)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
    return '''
    <!doctype html>
    <title>Upload to Model</title>
    <h2>Upload File</h2>
    <form method=post enctype=multipart/form-data>
    <p><input type=file name=file accept=image/* multiple>
    <input type=submit value=Upload>
    </form>
    '''


app.run(port=1337, host='0.0.0.0')