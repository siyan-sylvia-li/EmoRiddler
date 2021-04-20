from flask import Flask, render_template, session
from flask import request
from flask_session import Session
from flask_cors import CORS
app = Flask(__name__)

SECRET_KEY ='EmoRiddler'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/p0')
def pg0():
    return render_template('page_0.html')

@app.route('/p1')
def pg1():
    return render_template('page_1.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)