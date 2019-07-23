"""
    cookies的测试
"""
import datetime
from flask import Flask, make_response, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    outdate=datetime.datetime.today() + datetime.timedelta(days=2)
    data = {'name_1': 'index'}
    resp = make_response(jsonify(data))
    resp.set_cookie(
        'name', 
        'index', 
        expires=outdate,
        path='/index/')
    return resp


@app.route('/blog')
def blog():
    outdate=datetime.datetime.today() + datetime.timedelta(days=1)
    data = {'name_2': 'blog'}
    resp = make_response(jsonify(data))
    resp.set_cookie(
        'name', 
        'blog', 
        expires=outdate,
        domain='127.0.0.1')
    return resp


@app.route('/content')
def content():
    outdate=datetime.datetime.today() + datetime.timedelta(days=2)
    data = {'name': 'content'}
    resp = make_response(jsonify(data))
    resp.set_cookie(
        'name', 
        'content', 
        expires=outdate,
        domain='127.0.0.1',
        path='/content/')
    return resp


if __name__ == '__main__':
    app.run()