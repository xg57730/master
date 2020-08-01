'''
又是找BUG的一天
班级:1907B
日期:{2020/8/1}
阶段：Python高级

'''
'''
又是找BUG的一天
班级:1907B
日期:{2020/6/28}
阶段：Python高级

'''
from flask import Flask, redirect
import pymysql
from flask import request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import random
import requests
import time

from pymongo import MongoClient
import redis
from app import celery
# mongoDB
conn = MongoClient()
db = conn.md
table = db.socket_message
table1 = db.time_all
table2 = db.demo

# redis
r = redis.Redis('127.0.0.1', 6379)

pymysql.install_as_MySQLdb()
app = Flask(__name__)
CORS(app, cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins='*')


@celery.task
def watch_timing_send():
    lists = []
    for item in range(8):
        number = random.randint(1, 99)
        lists.append(number)
    print(lists)
    requests.get('http://127.0.0.1:5000/sendback', params={'lists': str(lists)})


@app.route('/save', methods=['GET', 'POST'])
def save_number():
    num_list = request.args.get('key_list')
    print(num_list)
    table2.insert_one({'number': num_list})
    return jsonify({'code': 200, 'msg': '存储成功'})
# 定时获取任务
@app.route('/sendback', methods=['GET', "POST"])
def send_back():
    num_list = request.args.get('lists')
    print(num_list)
    r.set('new_number_list', num_list)
    socketio.emit('sendback', eval(num_list))
    return "ok"



@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
