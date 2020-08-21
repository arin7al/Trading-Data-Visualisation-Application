import time
from flask import Flask, Response
from flask_cors import CORS
import numpy, random
from datetime import datetime, timedelta
import json
from RandomDealData import *

app = Flask(__name__)
CORS(app)

def index():
    return "Data Generator is running..."

def testservice():
    rdd = RandomDealData()
    deal = rdd.createRandomData( rdd.createInstrumentList() )
    return Response( deal, status=200, mimetype='application/json')

def stream():
    rdd = RandomDealData()
    instrList = rdd.createInstrumentList()
    def eventStream():
        while True:
            #nonlocal instrList
            yield rdd.createRandomData(instrList) + "\n"
    return Response(eventStream(), status=200, mimetype="text/event-stream")

def sse_stream():
    theHeaders = {"X-Accel-Buffering": "False"}
    rdd = RandomDealData()
    instrList = rdd.createInstrumentList()
    def eventStream():
        while True:
            #nonlocal instrList
            yield 'data:{}\n\n'.format(rdd.createRandomData(instrList))
    resp = Response(eventStream(), status=200, mimetype="text/event-stream")
    resp.headers["X-Accel-Buffering"] = "False"
    return resp


def get_time():
    """this could be any function that blocks until data is ready"""
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s


