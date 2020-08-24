from flask import Flask, Response, request, jsonify
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

    data = {"success": is_user_authenticated(username, password)}

    return jsonify(data)

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
