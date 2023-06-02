# encoding: utf-8
import time
import requests
from driver import driver


# from driver import driver

class Car:
    def __init__(self):
        self.car = driver()

    def setSpeed(self, x, y):
        self.car.set_speed(x, y)


def get_data():
    # 发起请求获取数据的逻辑
    response = requests.get('http://192.168.137.59:5000/GetVel')
    data = response.json()
    return data
    # 处理获取到的数据


# 执行定时任务
while True:
    velocity = get_data()
    fbV = velocity['transV'] / 2
    rtV = velocity['angleV'] / 5
    if abs(fbV) < 5:
        fbV = 0
    if abs(rtV) < 5:
        rtV = 0
    print(fbV,rtV)
    car = Car()
    car.setSpeed(fbV - rtV, fbV + rtV)
    time.sleep(0.1)
