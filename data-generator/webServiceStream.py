import time

import mysql.connector
from flask import Flask, Response
from flask_cors import CORS
import numpy, random
from datetime import datetime, timedelta
import json
from RandomDealData import *

app = Flask(__name__)
CORS(app)
config = {
    'user': 'root',
    'password': 'helloworld',
    'host': 'localhost',
    'port': 3308,
    'database': 'db_grad_cs_1917',
    'raise_on_warnings': True
}
cnx = mysql.connector.connect(**config)

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

def get_database_connection():
    return cnx

def save_in_database():
    cursor = cnx.cursor()
    # add_deal = ("INSERT INTO deal "
    #                 "(deal_id, deal_time, deal_counterparty_id, deal_instrument_id, deal_type, deal_amount, deal_quantity) "
    #                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    # data_deal = (1, "01", 2, 3, "A", 0, 0)
    # cursor.execute(add_deal, data_deal)
    add_user = ("INSERT INTO anonymous_users "
                     "(anonymous_user_id, anonymous_user_pwd) "
                     "VALUES (%s, %s)")
    data_user = ("1", "1")
    cursor.execute(add_user, data_user)
    cnx.commit()
    cursor.close()
    cnx.close()
