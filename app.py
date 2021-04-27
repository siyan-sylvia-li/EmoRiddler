import json
import os
import random
import time
import urllib.request
from multiprocessing import Pool
from threading import Thread

import cv2
from fer import FER
from fer.exceptions import InvalidImage
from flask import Flask, render_template, session
from flask import request
from flask_cors import CORS

from emotion_recognition.emotion_vote import emotion_voting
from flask_session import Session
from recommender_system import recommender_system

app = Flask(__name__)

SECRET_KEY ='EmoRiddler'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
CORS(app)

emotions = []
taskQueue = []
thresh = 0.1
bufferCount = 0
_pool = Pool(processes=4)
with open('static/random_positive.txt', 'r') as f:
    rand_responses = [x.replace("\n", "") for x in f.readlines()]


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

    def run(self):
        global emotions, taskQueue, thresh
        print("start")
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
        except InvalidImage:
            print("Invalid Image")
        except IndexError:
            print("Index Error")
        taskQueue.remove(x)
        print("done")
        return


def non_thread_emotion(img, buf, emots):
    with urllib.request.urlopen(img) as response:
        data = response.read()
    if os.path.exists("static/imgs/buffer" + str(buf) + ".png"):
        os.remove("static/imgs/buffer" + str(buf) + ".png")
    with open("static/imgs/buffer" + str(buf) + ".png", "wb+") as f:
        f.write(data)
    img_cv = cv2.imread("static/imgs/buffer" + str(buf) + ".png")
    try:
        detector = FER(mtcnn=True)
        print("DETECT")
        res = detector.detect_emotions(img_cv)
        print(res)
        if len(res):
            res = res[0]['emotions']
            emos = [e for e in res if res[e] > thresh]
            emots.extend(emos)
            # return emos
    except InvalidImage:
        print("Invalid Image")
    except IndexError:
        print("Index Error")
    # return []


def random_response():
    global rand_responses
    return random.choice(rand_responses)


@app.route('/')
def index():
    session['cond'] = 0
    return render_template('index.html')


@app.route('/c0')
def index0():
    session['cond'] = 0
    return render_template('index.html')


@app.route('/c1')
def index1():
    session['cond'] = 1
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
    return render_template('page_1.html', cond=str(session['cond']), partID=session['partID'])


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
    return render_template('final_page.html', score=str(score), cond=str(session['cond']), partID=session['partID'])


@app.route('/partID', methods=['POST'])
def partID():
    data = request.json
    session['partID'] = data['partID']
    return {'partID': session['partID']}


@app.route('/emotion', methods=['POST'])
def emotion():
    global bufferCount, emotions
    data = request.json
    img = data['usr_img']
    # Emotion recognition here
    """
        Threading
    """
    thread_a = Compute(img)
    thread_a.start()
    thread_a.join()
    """
        Multiprocessing
    """
    # f = _pool.apply_async(non_thread_emotion, [img, bufferCount])
    #
    # bufferCount = bufferCount + 1
    # r = f.get(timeout=10)
    # emotions.extend(r)

    """
        Processes
    """
    # p = Process(target=non_thread_emotion, args=(img, bufferCount, emotions))
    # bufferCount = bufferCount + 1
    # taskQueue.append(p)
    # p.start()
    # p.join()
    return {"res": "1"}


@app.route('/response', methods=['GET'])
def resp():
    global emotions, taskQueue, bufferCount
    """
        Threading
    """
    while len(taskQueue):
        time.sleep(1)

    """
        Multiprocessing
    """
    # for p in taskQueue:
    #     p.join(timeout=10)
    #     while p.is_alive():
    #         time.sleep(1)
    if session['cond'] == 0:
        emo_votes = emotion_voting(emotions)
        emotions = []
        # emo_votes = [x.lower() for x in emo_votes]
        resp = recommender_system.emotional_response(emo_votes)
    else:
        resp = random_response()
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
    try:
        # insert production server deployment code
        app.run(port=8001, debug=True)
    except KeyboardInterrupt:
        _pool.close()
        _pool.join()

