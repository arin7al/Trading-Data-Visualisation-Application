from flask import Flask, Response
from flask_cors import CORS
import webServiceStream
from RandomDealData import *
import sys

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


def bootapp(ip, port):
    #global rdd 
    #rdd = RandomDealData()
    #webServiceStream.bootServices()
    app.run(debug=True, port=port, threaded=True, host=(ip))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Web service need 2 arguments: ip address and port")
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    bootapp(host, port)
