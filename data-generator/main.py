from flask import Flask, Response, request
from flask_cors import CORS
import web_service_stream
from random_deal_data import *
import sys
from authentication import *

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return web_service_stream.index()

@app.route('/testservice')
def testservice():
    return web_service_stream.testservice()

@app.route('/streamTest')
def stream():
    return web_service_stream.stream()

@app.route('/streamTest/sse')
def sse_stream():
    return web_service_stream.sse_stream()

@app.route('/dbtest')
def dbtest():
    web_service_stream.save_in_database()
    return "hi"

@app.route('/authentication')
def authentication():
    username = request.args.get('username')
    password = request.args.get('password')

    return str(is_user_authenticated(username, password))

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
