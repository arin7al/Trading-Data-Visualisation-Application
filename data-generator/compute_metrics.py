import sys
import db
from random_deal_data import counterparty_dict, instrument_dict


class MetricsCalculator:
    def __init__(self):
        try:
            self.cnx = db.get_connection()
            self.cursor = self.cnx.cursor()

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()

    def calcAvgInstrumentPrice(self,instrument, start, stop):
        try:

            SQL_STATEMENT_BUY = ("SELECT AVG(deal_price) FROM deal "
                                 "WHERE deal_type = 'B' AND"
                                 "deal_time BETWEEN {} AND {} AND"
                                 "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(start, stop, instrument)
            SQL_STATEMENT_SELL = ("SELECT AVG(deal_price) FROM deal "
                                  "WHERE deal_type = 'S' AND"
                                  "deal_time BETWEEN {} AND {} AND"
                                  "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(start, stop, instrument)

            self.cursor.execute(SQL_STATEMENT_BUY)
            result = self.cursor.fetchone()
            self.cursor.execute(SQL_STATEMENT_SELL)
            result2 = self.cursor.fetchone()
            return result[0], result2[0]

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()

    def calcAvgInstrumentBuyPriceForAllTime(self, instrument):
        try:

            SQL_STATEMENT_BUY = ("SELECT AVG(deal_price) FROM deal "
                                 "WHERE deal_type = 'B' AND "
                                 "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(instrument)

            self.cursor.execute(SQL_STATEMENT_BUY)
            result = self.cursor.fetchone()

            return result[0]

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
            return None, None

    def calcAvgInstrumentSellPriceForAllTime(self, instrument):
        try:
            SQL_STATEMENT_SELL = ("SELECT AVG(deal_price) FROM deal "
                                  "WHERE deal_type = 'S' AND "
                                  "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(instrument)

            self.cursor.execute(SQL_STATEMENT_SELL)
            result = self.cursor.fetchone()
            return result[0]

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
            return None, None

    def calcEndPosition(self):
        end_position_list = []
        try:
            for counterparty_name, counterparty_id in counterparty_dict.items():
                position_dict = {'cpty_name':counterparty_name}
                for instrument_name, instrument_id in instrument_dict.items():
                    SQL_STATEMENT_BUY = ("SELECT SUM(deal_quantity) FROM deal "
                                         "WHERE deal_type = 'B' AND "
                                         "deal_instrument_id = {} AND deal_counterparty_id = {}").format(instrument_id, counterparty_id)
                    SQL_STATEMENT_SELL = ("SELECT SUM(deal_quantity) FROM deal "
                                         "WHERE deal_type = 'S' AND "
                                         "deal_instrument_id = {} AND deal_counterparty_id = {}").format(instrument_id, counterparty_id)
                    self.cursor.execute(SQL_STATEMENT_BUY)
                    result = self.cursor.fetchone()
                    sum_of_buys = result[0]
                    if sum_of_buys is None:
                        sum_of_buys = 0
                    self.cursor.execute(SQL_STATEMENT_SELL)
                    result1 = self.cursor.fetchone()
                    sum_of_sells = result1[0]
                    if sum_of_sells is None:
                        sum_of_sells = 0
                    position_dict[instrument_name] = float(sum_of_buys - sum_of_sells)
                    #        also calculate cash?
                end_position_list.append(position_dict)
            return end_position_list
        #       return list of maps
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()