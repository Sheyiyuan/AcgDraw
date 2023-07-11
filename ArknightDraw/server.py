# -*- encoding:utf-8 -*-
import os

from flask import Flask, send_file
import ArknightDraw.drawHandleArk
# import numpy as np
import io
from gevent import pywsgi

app = Flask(__name__)


@app.route("/arknights/arknightsdraw", methods=['POST', 'GET'])
def arknights():
    img = ArknightDraw.drawHandleArk.ten_draw()
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


@app.route('/', methods=['POST', 'GET'])
def arknights_draw():
    img = ArknightDraw.drawHandleArk.ten_draw()
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


def server_start(mode="", host="127.0.0.1", port=11451):
    if mode == "debug":
        app.run(debug=True)
        print("测试环境")
    else:
        try:
            print("图片服务器已启动：http://" + host + ":" + str(port))
            server = pywsgi.WSGIServer((host, port), app)
            server.serve_forever()
        except OSError:
            print("端口被占用，请修改端口")

if __name__ == "__main__":
    server_start()
