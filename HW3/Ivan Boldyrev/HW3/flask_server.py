from flask import Flask, request


def factorial(n):
    fac = 1
    while n > 1:
        fac *= n
        n -= 1
    return fac


app = Flask(__name__)


@app.route('/factorial', methods=['GET'])
def get_factorial():
    n = int(request.args['n'])
    return str(factorial(n))


@app.route("/num")
def get_num():
    return "10"


@app.route("/")
def main_page():
    return "<p>Welcome to Flask!</p>"


if __name__ == '__main__':
    app.run()
