import ast
import sys
from datetime import datetime

import db
from metricsCalculator import MetricsCalculator
from random_deal_data import RandomDealData


def test_average_price_is_calculated():
    # fill in database
    try:
        cnx = db.get_connection()
        cursor = cnx.cursor()
        insert_instrument = "INSERT INTO instrument (instrument_id, instrument_name) VALUES (5000, 'test_instrument')"
        cursor.execute(insert_instrument)
        cnx.commit()

        insert_deal = "INSERT INTO deal (deal_id, deal_time, deal_instrument_id, deal_type, deal_price, deal_quantity) VALUES (%s, %s, %s, %s, %s, %s)"
        deal_info = (1, datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"), 5000, 'S', 100.0, 1)
        cursor.execute(insert_deal, deal_info)
        cnx.commit()

        deal_info = (2, '23-Aug-2020 (11:52:42.480671)', 5000, 'S', 300.0, 1)
        cursor.execute(insert_deal, deal_info)
        cnx.commit()

        deal_info = (3, '23-Aug-2020 (11:52:42.480671)', 5000, 'B', 400.0, 1)
        cursor.execute(insert_deal, deal_info)
        cnx.commit()

        deal_info = (4, '23-Aug-2020 (11:52:42.480671)', 5000, 'B', 600.0, 1)
        cursor.execute(insert_deal, deal_info)
        cnx.commit()
        cursor.close()
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        print()


    # calculate metrics
    calculator = MetricsCalculator()
    avg_buy_price, avg_sell_price = calculator.calcAvgInstrumentPriceForAllTime('test_instrument')

    # clean database
    try:
        cnx = db.get_connection()
        cursor = cnx.cursor()
        delete_rows = "DELETE FROM instrument WHERE instrument_id = 5000"
        cursor.execute(delete_rows)
        delete_rows = "DELETE FROM deal WHERE deal_instrument_id = 5000"
        cursor.execute(delete_rows)
        cnx.commit()
        cursor.close()
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        print()
    # make asserts
    assert avg_buy_price == 500.0
    assert avg_sell_price == 200.0

#test rpl

def test_realized_profit_is_calculated():
    # fill in database
    try:
        cnx = db.get_connection()
        cursor = cnx.cursor()
        insert_instrument = "INSERT INTO instrument (instrument_id, instrument_name) VALUES (5000, 'test_instrument')"
        cursor.execute(insert_instrument)
        cnx.commit()

        insert_deal = "INSERT INTO deal (deal_id, deal_time, deal_instrument_id, deal_type, deal_price, deal_quantity) VALUES (%s, %s, %s, %s, %s, %s)"
        deal_info = (1, datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"), 5000, 'S', 100.0, 1)
        cursor.execute(insert_deal, deal_info)
        cnx.commit()

        deal_info = (2, '23-Aug-2020 (11:52:42.480671)', 5000, 'S', 300.0, 1)
        cursor.execute(insert_deal, deal_info)
        cnx.commit()

        deal_info = (3, '23-Aug-2020 (11:52:42.480671)', 5000, 'B', 400.0, 1)
        cursor.execute(insert_deal, deal_info)
        cnx.commit()

        deal_info = (4, '23-Aug-2020 (11:52:42.480671)', 5000, 'B', 600.0, 1)
        cursor.execute(insert_deal, deal_info)
        cnx.commit()
        cursor.close()
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        print()

# calculate metrics
    calculator = MetricsCalculator()
    realizedProfit = calculator.calcRealizedProfit()

    # clean database
    try:
        cnx = db.get_connection()
        cursor = cnx.cursor()
        delete_rows = "DELETE FROM instrument WHERE instrument_id = 5000"
        cursor.execute(delete_rows)
        delete_rows = "DELETE FROM deal WHERE deal_instrument_id = 5000"
        cursor.execute(delete_rows)
        cnx.commit()
        cursor.close()
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        print()
    # make asserts
    print(realizedProfit)
    #assert realizedProfit == -600

if __name__ == "__main__":
    #test_average_price_is_calculated()
    test_realized_profit_is_calculated()

