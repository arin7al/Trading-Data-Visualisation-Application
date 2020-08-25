from flask import Flask, render_template, Response, request, json, jsonify, make_response
from flask_sse import sse
from flask_cors import CORS
import requests
import time
import sys

app = Flask(__name__)
#app.register_blueprint(sse, url_prefix='/stream')
CORS(app)

@app.route('/deals')
def forwardStream():
    rest_url = datagen_url + "/streamTest"
    r = requests.get(rest_url, stream=True)
    def eventStream():
            for line in r.iter_lines( chunk_size=1):
                if line:
                    yield 'data:{}\n\n'.format(line.decode())
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/client/testservice')
def client_to_server():
    rest_url = datagen_url + "/streamTest"
    r = requests.get(rest_url)
    return Response(r.iter_lines(chunk_size=1), mimetype="text/json")

@app.route('/')
@app.route('/index')
def index():
    return "webtier service points are running..."

@app.route('/connection')
def connection():
    rest_url = datagen_url + "/"
    data = {}
    try:
        requests.get(rest_url)
        data = {'connected': True}
    except:
        data = {'connected': False}

    return jsonify(data)

@app.route('/authentication')
def authentication():
    rest_url = datagen_url + "/authentication"

    username = request.args.get('username')
    password = request.args.get('password')

    rest_url += "?username=" + username + "&password=" + password

    r = requests.get(rest_url)

    success = r.json()

    return success

@app.route("/metrics/average/sell-buy")
def average():
    rest_url_sell = datagen_url + "/metrics/average/sell"
    rest_url_buy = datagen_url + "/metrics/average/buy"

    instrument = request.args.get('instrument')

    r_sell = requests.get(rest_url_sell + '?instrument=' + instrument)
    r_buy = requests.get(rest_url_buy + '?instrument=' + instrument)

    sell = r_sell.json()
    buy = r_buy.json()

    data = {"sell" : sell, "buy": buy}

    return jsonify(data)

@app.route('/metrics')
def metrics():
    rest_url_realized_profit = datagen_url + "/metrics/profit/realized"
    rest_url_effective_profit = datagen_url + "/metrics/profit/effective"
    rest_url_end_position = datagen_url + "/metrics/end-position"

    r_realized = requests.get(rest_url_realized_profit)
    r_effective = requests.get(rest_url_effective_profit)
    r_end_position = requests.get(rest_url_end_position)

    realized = r_realized.json()
    effective = r_effective.json()
    end_position = r_end_position.json()



    data = {"realized": realized,
            "effective": effective,
            "end-position": end_position}

    return jsonify(data)

def get_message():
    """this could be any function that blocks until data is ready"""
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s

def bootapp(ip, port):
    app.run(port=port, threaded=True, host=ip)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Web service need 4 arguments: web server ip address, port and datagen ip address, port")
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    datagen_ip = sys.argv[3]
    datagen_port = int(sys.argv[4])

    global datagen_url
    datagen_url = "http://" + datagen_ip + ":" + str(datagen_port)

    bootapp(host, port)
