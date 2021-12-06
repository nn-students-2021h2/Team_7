# -*- coding: utf-8 -*-
from flask import Flask, request

from get_fibonacci import get_fibonacci_value

app = Flask(__name__)


@app.route('/')
def main_page():
    pass


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    n = int(request.args['n'])
    return get_fibonacci_value(n)


@app.route('/echo', methods=['GET'])
def echo():
    return 'OK'


if __name__ == '__main__':
    app.run()
