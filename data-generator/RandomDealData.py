import sys
import time
import numpy, random
from datetime import datetime, timedelta
import json
from Instrument import *
import db

instruments = ("Astronomica", "Borealis", "Celestial", "Deuteronic", "Eclipse",
			"Floral", "Galactia", "Heliosphere", "Interstella", "Jupiter", "Koronis", "Lunatic")
counterparties = ("Lewis", "Selvyn", "Richard", "Lina", "John", "Nidia")
NUMBER_OF_RANDOM_DEALS = 2000
TIME_PERIOD_MILLIS = 3600000
EPOCH = datetime.now() - timedelta(days = 1)


class RandomDealData:
    def saveCptysToDatabase(self):
        try:
            cnx = db.get_connection()
            add_cpty = ("INSERT INTO counterparty "
                                  "(counterparty_id, counterparty_name) "
                                  "VALUES (%s, %s)")
            id = 1
            for cpty in counterparties:
                cursor = cnx.cursor()
                data_cpty = (id,cpty)
                cursor.execute(add_cpty, data_cpty)
                cnx.commit()
                cursor.close()
                id = id + 1
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()

    def createInstrumentList(self):
        self.saveCptysToDatabase()
        f = open('initialRandomValues.txt', 'r')
        instrumentId = 1000
        instrumentList = []
        for instrumentName in instruments:
            hashedValue = int(f.readline())
            isNegative = hashedValue < 0
            basePrice = (abs(hashedValue) % 10000) + 90.0
            drift = ((abs(hashedValue) % 5) * basePrice) / 1000.0
            drift = 0 - drift if isNegative else drift
            variance = (abs(hashedValue) % 1000) / 100.0
            variance = 0 - variance if isNegative else variance
            instrument = Instrument(instrumentId, instrumentName, basePrice, drift, variance)
            self.saveInstrumentToDatabase(instrument)
            instrumentList.append(instrument)
            instrumentId += 1
        return instrumentList

    def saveInstrumentToDatabase(self, instrument):
        try:
            cnx = db.get_connection()
            cursor = cnx.cursor()
            add_instrument = ("INSERT INTO instrument "
                              "(instrument_id, instrument_name) "
                              "VALUES (%s, %s)")
            data_instrument = (instrument.id, instrument.name)
            cursor.execute(add_instrument, data_instrument)
            cnx.commit()
            cursor.close()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()

    def createRandomData( self, instrumentList ):
        time.sleep(random.uniform(1,30)/100)
        dealId = 20000
        instrument = instrumentList[numpy.random.randint(0,len(instrumentList))]
        cpty = counterparties[numpy.random.randint(0,len(counterparties))]
        type = 'B' if numpy.random.choice([True, False]) else 'S'
        quantity = int( numpy.power(1001, numpy.random.random()))
        dealTime = datetime.now() - timedelta(days = 1)
        dealId += 1
        deal = {
            'instrumentName' : instrument.name,
            'cpty' : cpty,
            'price' : instrument.calculateNextPrice(type),
            'type' : type,
            'quantity' : quantity,
            'time' : dealTime.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
            }
        return json.dumps(deal)

