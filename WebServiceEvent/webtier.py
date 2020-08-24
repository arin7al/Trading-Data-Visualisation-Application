from flask import Flask, render_template, Response
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
    try:
        requests.get(rest_url)
        return "true"
    except:
        return "false"

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