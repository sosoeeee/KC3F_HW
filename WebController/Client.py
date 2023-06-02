import time
import requests


def get_data():
    # 发起请求获取数据的逻辑
    response = requests.get('http://localhost:5000/GetVel')
    data = response.json()
    print(data)
    # 处理获取到的数据


# 执行定时任务
while True:
    get_data()
    time.sleep(0.1)
