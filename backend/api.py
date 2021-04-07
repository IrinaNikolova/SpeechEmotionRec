import json
import os
import flask
from flask_cors import CORS, cross_origin
from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from backend import main

app = flask.Flask(__name__)
CORS(app)

filename: str = ''
tips: dict = {
    'neutral': 'A good strategy to connect with the audience is to frequently make eye contact. Looking at the '
               'audience is beneficial for forging a good connection between you and the people.\nWalking while you '
               'speaking is a way to break the barriers between you and the audience. It represents that you are '
               'grounded and claim what you are saying.',
    'calm': 'Great job! Being calm shows confidence to the audience.\nBe aware of your body language because your '
            'gestures are signature for your attitude to the topic and the audience.',
    'happy': 'Great job! Being happy and cheerful shows enthusiasm to the topic you are presenting.\nBe aware of '
             'your body language because your gestures are signature for your attitude to the topic and the audience.',
    'sad': 'Visualize your success could be very powerful. Thus, you will gain more courage because everyone could '
           'be a good public speaker.\nPractice your speech a significant number of times because practice makes '
           'perfect. The more prepared you are, the more confident you will be despite side factors that could make '
           'you feel sad.',
    'angry': 'Practice your speech a significant number of times because practice makes perfect. The more prepared '
             'you are, the more confident you will be despite side factors that could make you feel angry.\nLearn to '
             'accept that someone or something can always make you annoyed before your speech. Then remember your set '
             'goals and try to disregard yourself from the distractions that make you angry.\nMeditation before '
             'public speaking is always a reasonable decision. It will make you calmer and more focused on your goal.',
    'fearful': 'Don’t try to fully get rid of your nervousness. It is inevitable. However, try to convert it into '
               'excitement and apply the adrenaline to your benefit.\nTry to project your voice. To achieve a '
               'naturally booming tone of your voice take a relaxed deep-breath every time before you have a new '
               'passage.\nConsidering your audience is a key to reduce the stress. Don’t focus only on yourself '
               'because public speaking is a two-sided process. It should be intriguing, entertaining and at the same '
               'time beneficial for the listeners.',
    'disgust': 'Visualize your success could be very powerful. Thus, you will gain more courage because everyone '
               'could be a good public speaker.\nLearn to accept that not everything will be to your affinity. Then '
               'remember your goals and try to disregard yourself and perform as good as possible.',
    'surprised': 'Practice your speech a significant number of times because practice makes perfect. The more '
                 'prepared you are, the more confident you will be in case you receive an unexpected question from '
                 'the audience. Therefore, you scale down the risk of getting surprised .\nConsidering your audience '
                 'is crucial. Don’t focus only on yourself because public speaking is a two-sided process. The more '
                 'you know about your audience, the lower will be the chance to receive a surprising question '
}

# checking if the uploaded file is not malisous, if the the last extention is wav, not py (or not disgaised as another file) and is not executable
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
    path_file: str = path + '\\' + filename
    result = main.analyse_file(path_file)
    json_result: dict = {
        'emotion': result[0],
        'tips': tips[result[0]]
    }
    return jsonify(json_result)


if __name__ == '__main__':
    app.run()
