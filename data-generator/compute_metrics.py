import sys
import db


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

    def calcAvgInstrumentPriceForAllTime(self, instrument):
        try:

            SQL_STATEMENT_BUY = ("SELECT AVG(deal_price) FROM deal "
                                 "WHERE deal_type = 'B' AND "
                                 "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(instrument)
            SQL_STATEMENT_SELL = ("SELECT AVG(deal_price) FROM deal "
                                  "WHERE deal_type = 'S' AND "
                                  "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(instrument)

            self.cursor.execute(SQL_STATEMENT_BUY)
            result = self.cursor.fetchone()
            self.cursor.execute(SQL_STATEMENT_SELL)
            result2 = self.cursor.fetchone()
            return result[0], result2[0]

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
            return None, None

