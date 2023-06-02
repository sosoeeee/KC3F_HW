# encoding: utf-8
from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
V = {'transV': 0, 'angleV': 0}


# URL路由与视图函数
@app.route('/PE/Control')
def PEJoyStick():
    return render_template('peJoyStick.html')


@app.route('/')
def index():
    return 'Hello World'


@app.route('/GetVel', methods=['GET'])
def vel():
    global V
    return jsonify(V)


@app.route('/send-transV', methods=['POST'])
def get_transV():
    global V
    message = request.form.get('transV')
    # 在这里对接收到的消息进行处理
    V['transV'] = float(message)
    print('Received transV:', message)
    return 'Message received'


@app.route('/send-angleV', methods=['POST'])
def get_angleV():
    global V
    message = request.form.get('angleV')
    # 在这里对接收到的消息进行处理
    V['angleV'] = float(message)
    print('Received angleV:', message)
    return 'Message received'


# app.run(host='0.0.0.0', port=3009)
app.run(host='192.168.137.59')
