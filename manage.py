#!/usr/bin/env python3
import os
from app import create_app
from flask_script import Manager, Server
from gevent import monkey
from gevent.pywsgi import WSGIServer
# 下面这句不加也能启动服务，但是你会发现Flask还是单线程，在一个请求未返回时，其他请求也会阻塞，所以请添加这句
monkey.patch_all()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# manager = Manager(app)

# server = Server(host="0.0.0.0", port=5000,threaded=True)
# manager.add_command("runserver", server)
http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()

# @manager.command
# def test():
#     import unittest
#     tests = unittest.TestLoader().discover('production')
#     unittest.TextTestRunner(verbosity=2).run(tests)
#
#
# if __name__ == '__main__':
#     manager.run()
