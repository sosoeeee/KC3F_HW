from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# URL路由与视图函数
@app.route('/hello')
def hello():
    return 'Hello World'


@app.route('/PE/Control')
def PEJoyStick():
    return render_template('peJoyStick.html')


@app.route('/PC/Control')
def PCJoyStick():
    return render_template('pcJoyStick.html')


@app.route('/')
def index():
    return render_template('test.html')


@app.route('/send-message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    # 在这里对接收到的消息进行处理
    print('Received message:', message)
    return 'Message received'


@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    # 可以在这里对接收到的信息进行处理


# app.run(host='0.0.0.0', port=3009)
socketio.run(app, host='0.0.0.0', allow_unsafe_werkzeug=True)
