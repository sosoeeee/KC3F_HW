from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello World'


@app.route('/JoyStick')
def JoyStick():
    return render_template('JoyStick.html')


@app.route('/Button', methods=['get'])
def Button():
    return render_template('Button2.html')


@app.route('/Button', methods=['post'])
def ButtonState():
    # button_status = request.form['button_status']
    # Do something with button_status
    return request.form  # 'Button status is {}'.format(button_status)


@app.route('/GetButton', methods=['get', 'post'])
def GetButton():
    button_status = request.form['button_status']
    return 'Button status is: ' + button_status
    # return 'Got'


@app.route('/submit-form', methods=['GET', 'POST'])
def submit_form():
    for key in request.form:
        print(key)
    return 'Form fields printed to console'


# app.run(host='0.0.0.0', port=3009)
socketio.run(app, host='0.0.0.0', port=3009, allow_unsafe_werkzeug=True)
