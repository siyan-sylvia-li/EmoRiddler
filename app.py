import threading
import time

from flask import Flask, render_template, session
from flask import request
from flask_session import Session
from flask_cors import CORS
import json
from recommender_system import recommender_system
from emotion_recognition.emotion_recognition import emotion_recognition
from emotion_recognition.emotion_vote import emotion_voting
from threading import Thread
import urllib.request
from fer import FER
from fer.exceptions import InvalidImage
import cv2

app = Flask(__name__)
emotions = []
taskQueue = []

SECRET_KEY ='EmoRiddler'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
CORS(app)


class Compute(Thread):
    def __init__(self, img):
        Thread.__init__(self)
        self.img = img
        with urllib.request.urlopen(img) as response:
            data = response.read()
        with open("static/imgs/buffer.png", "wb+") as f:
            f.write(data)
        self.img_cv = cv2.imread("static/imgs/buffer.png")
        #     data = 'data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUAAAhwAAAFoCAYAAAA.......'
        # response = urllib.request.urlopen(data)
        # with open('image.jpg', 'wb') as f:
        #     f.write(response.file.read())

    def run(self):
        global emotions, taskQueue
        print("start")
        # emo_labels = emotion_recognition(self.img)
        # session['emotions'].extend(emo_labels)
        x = len(taskQueue)
        taskQueue.append(x)
        try:
            detector = FER(mtcnn=True)
            emo, score = detector.top_emotion(self.img_cv)
            print("DETECT")
            print(detector.detect_emotions(self.img_cv))
            emotions.append(emo)
        except InvalidImage:
            print("Invalid Image")
        taskQueue.remove(x)
        print("done")
        return


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/p0')
def pg0():
    global emotions
    session['time'] = 0
    emotions = []
    return render_template('page_0.html')


@app.route('/p1')
def pg1():
    return render_template('page_1.html')


@app.route('/p2')
def pg2():
    return render_template('page_2.html')


@app.route('/feedback')
def feedback():
    session['time'] = session['time'] + 1
    return render_template('feedback.html', partID=session['partID'], time=str(session['time']))


@app.route('/partID', methods=['POST'])
def partID():
    data = request.json
    session['partID'] = data['partID']
    return {'partID': session['partID']}


def non_thread_emotion(img):
    global emotions
    with urllib.request.urlopen(img) as response:
        data = response.read()
    with open("static/imgs/buffer.png", "wb+") as f:
        f.write(data)
    print("start")
    # emo_labels = emotion_recognition(self.img)
    # session['emotions'].extend(emo_labels)
    img = cv2.imread("static/imgs/buffer.png")
    detector = FER(mtcnn=True)
    emo, score = detector.top_emotion(img)
    emotions.append(emo)
    print("done")


@app.route('/emotion', methods=['POST'])
def emotion():
    data = request.json
    img = data['usr_img']
    # Emotion recognition here
    thread_a = Compute(img)
    thread_a.start()
    # thread_a.join()
    # non_thread_emotion(img)
    return {"res": "1"}


@app.route('/response', methods=['GET'])
def resp():
    global emotions, taskQueue
    while len(taskQueue):
        time.sleep(3)
    emo_votes = emotion_voting(emotions)
    emotions = []
    emo_votes = [x.lower() for x in emo_votes]
    resp = recommender_system.emotional_response(emo_votes)
    return {"response": resp}


@app.route('/question')
def question():
    questNum = int(request.args.get('questNum'))
    with open('static/questions/q' + str(questNum) + '.json') as f:
        quest = json.load(f)
    return render_template('question.html', questionNum=str(questNum),
                           question=quest['question'],
                           choiceA=quest['choiceA'],
                           choiceB=quest['choiceB'],
                           choiceC=quest['choiceC'],
                           choiceD=quest['choiceD'],
                           correct=quest['correct'])

if __name__ == '__main__':
    app.run(port=8000, debug=True)