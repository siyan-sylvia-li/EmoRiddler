import threading
import time, os

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
thresh = 0.05
bufferCount = 0

SECRET_KEY ='EmoRiddler'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
CORS(app)


class Compute(Thread):
    def __init__(self, img):
        global bufferCount
        Thread.__init__(self)
        self.img = img
        with urllib.request.urlopen(img) as response:
            data = response.read()
        if os.path.exists("static/imgs/buffer" + str(bufferCount) + ".png"):
            os.remove("static/imgs/buffer" + str(bufferCount) + ".png")
        with open("static/imgs/buffer" + str(bufferCount) + ".png", "wb+") as f:
            f.write(data)
        self.img_cv = cv2.imread("static/imgs/buffer" + str(bufferCount) + ".png")
        bufferCount = bufferCount + 1
        #     data = 'data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUAAAhwAAAFoCAYAAAA.......'
        # response = urllib.request.urlopen(data)
        # with open('image.jpg', 'wb') as f:
        #     f.write(response.file.read())

    def run(self):
        global emotions, taskQueue, thresh
        print("start")
        # emo_labels = emotion_recognition(self.img)
        # session['emotions'].extend(emo_labels)
        x = len(taskQueue)
        taskQueue.append(x)
        try:
            detector = FER(mtcnn=True)
            print("DETECT")
            res = detector.detect_emotions(self.img_cv)
            print(res)
            if len(res):
                res = res[0]['emotions']
                emos = [e for e in res if res[e] > thresh]
                emotions.extend(emos)
            # emo, score = detector.top_emotion(self.img_cv)
            # emotions.append(emo)
        except InvalidImage:
            print("Invalid Image")
        except IndexError:
            print("Index Error")
        taskQueue.remove(x)
        print("done")
        return


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/p0')
def pg0():
    global emotions, bufferCount
    session['time'] = 0
    bufferCount = 0
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


@app.route('/final')
def final():
    score = request.args.get('count')
    return render_template('final_page.html', score=str(score))


@app.route('/partID', methods=['POST'])
def partID():
    data = request.json
    session['partID'] = data['partID']
    return {'partID': session['partID']}


@app.route('/emotion', methods=['POST'])
def emotion():
    global bufferCount
    data = request.json
    img = data['usr_img']
    # Emotion recognition here
    thread_a = Compute(img)
    thread_a.start()
    thread_a.join()
    # non_thread_emotion(img)
    return {"res": "1"}


@app.route('/response', methods=['GET'])
def resp():
    global emotions, taskQueue, bufferCount
    while len(taskQueue):
        time.sleep(1)
    emo_votes = emotion_voting(emotions)
    emotions = []
    emo_votes = [x.lower() for x in emo_votes]
    resp = recommender_system.emotional_response(emo_votes)
    bufferCount = 0
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


@app.route('/small_question')
def small_question():
    questNum = int(request.args.get('questNum'))
    with open('static/questions/q' + str(questNum) + '.json') as f:
        quest = json.load(f)
    return render_template('small_question.html', questionNum=str(questNum),
                           question=quest['question'],
                           choiceA=quest['choiceA'],
                           choiceB=quest['choiceB'],
                           choiceC=quest['choiceC'],
                           choiceD=quest['choiceD'],
                           correct=quest['correct'])


@app.route('/long_question')
def long_question():
    questNum = int(request.args.get('questNum'))
    with open('static/questions/q' + str(questNum) + '.json') as f:
        quest = json.load(f)
    return render_template('long_question.html', questionNum=str(questNum),
                           question=quest['question'],
                           choiceA=quest['choiceA'],
                           choiceB=quest['choiceB'],
                           choiceC=quest['choiceC'],
                           choiceD=quest['choiceD'],
                           correct=quest['correct'])

if __name__ == '__main__':
    app.run(port=8000, debug=True)