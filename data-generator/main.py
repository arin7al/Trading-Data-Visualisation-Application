from flask import Flask, Response, request
from flask_cors import CORS
import webServiceStream
from RandomDealData import *
import sys
from authentication import *

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return webServiceStream.index()

@app.route('/testservice')
def testservice():
    return webServiceStream.testservice()

@app.route('/streamTest')
def stream():
    return webServiceStream.stream()

@app.route('/streamTest/sse')
def sse_stream():
    return webServiceStream.sse_stream()

@app.route('/dbtest')
def dbtest():
    webServiceStream.save_in_database()
    return "hi"

@app.route('/authentication')
def authentication():
    username = request.args.get('username')
    password = request.args.get('password')

    return str(is_user_authenticated(username, password))

@app.route('/metrics/average/sell')
def sell_average():
    instrument = request.args.get('instrument')
    return str(1)

@app.route('/metrics/average/buy')
def buy_average():
    instrument = request.args.get('instrument')
    return str(2)


def bootapp(ip, port):
    #global rdd 
    #rdd = RandomDealData()
    #webServiceStream.bootServices()
    app.run(debug=True, port=port, threaded=True, host=ip)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Web service need 2 arguments: ip address and port")
        sys.exit()

    ip = sys.argv[1]
    port = int(sys.argv[2])

    bootapp(ip, port)
