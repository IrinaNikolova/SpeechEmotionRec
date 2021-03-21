import json
import os
import flask
from flask_cors import CORS, cross_origin
from flask import request
from werkzeug.exceptions import BadRequest
import main

app = flask.Flask(__name__)
CORS(app)

filename: str = ''


def sanity_check(file_name: str) -> bool:
    elems: list = file_name.split('.')
    if elems[len(elems) - 1] != 'wav':
        return True
    return False


@app.route('/file', methods=['POST'])
@cross_origin()
def analyze_file() -> str:
    global filename
    file = request.files['file']
    path = 'C:\\University\\3rd year\\3rd Year Project\\SpeechEmotionRec\\interview_recordings'
    file.save(os.path.join(path, file.filename))
    filename = file.filename
    suspicious: bool = sanity_check(filename)
    if suspicious:
        raise BadRequest('The file should be .wav!')
    return json.dumps({'success': True})


if __name__ == '__main__':
    app.run()
