import sys
import db
from random_deal_data import counterparty_dict, instrument_dict


class MetricsCalculator:


    def calcAvgInstrumentPrice(self,instrument, start, stop):
        try:
            cnx = db.get_connection()
            cursor = cnx.cursor()
            SQL_STATEMENT_BUY = ("SELECT AVG(deal_price) FROM deal "
                                 "WHERE deal_type = 'B' AND"
                                 "deal_time BETWEEN {} AND {} AND"
                                 "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(start, stop, instrument)
            SQL_STATEMENT_SELL = ("SELECT AVG(deal_price) FROM deal "
                                  "WHERE deal_type = 'S' AND"
                                  "deal_time BETWEEN {} AND {} AND"
                                  "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(start, stop, instrument)

            cursor.execute(SQL_STATEMENT_BUY)
            result = cursor.fetchone()
            cursor.execute(SQL_STATEMENT_SELL)
            result2 = cursor.fetchone()
            cnx.commit()
            cursor.close()
            return result[0], result2[0]

        except:
            print("Couldn't calcAvgInstrumentPrice, ", sys.exc_info()[0], "occurred.")
            print()

    def calcAvgInstrumentBuyPriceForAllTime(self, instrument):
        try:
            cnx = db.get_connection()
            cursor = cnx.cursor()
            SQL_STATEMENT_BUY = ("SELECT AVG(deal_price) FROM deal "
                                 "WHERE deal_type = 'B' AND "
                                 "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(instrument)

            cursor.execute(SQL_STATEMENT_BUY)
            result = cursor.fetchone()
            cnx.commit()
            cursor.close()
            return result[0]

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
            return None, None

    def calcAvgInstrumentSellPriceForAllTime(self, instrument):
        try:
            cnx = db.get_connection()
            cursor = cnx.cursor()
            SQL_STATEMENT_SELL = ("SELECT AVG(deal_price) FROM deal "
                                  "WHERE deal_type = 'S' AND "
                                  "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = '{}')").format(instrument)

            cursor.execute(SQL_STATEMENT_SELL)
            result = cursor.fetchone()
            cnx.commit()
            cursor.close()
            return result[0]

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
            return None, None
    #
    # def calcRealizedProfit(self):
    #     RealizedProfit = 0.
    #
    #     try:
    #         SQL_STATEMENT_DEAL_IDS = ("SELECT DISTINCT deal_instrument_id FROM deal ")
    #         self.cursor.execute(SQL_STATEMENT_DEAL_IDS)
    #         instruments_ids = self.cursor.fetchone()[0]
    #         for instrument in instruments_ids:
    #             SQL_STATEMENT_BUY = ("SELECT deal_price, deal_quantity FROM deal "
    #                                  "WHERE deal_type = 'B' "
    #                                  " deal_instrument_id = {} ").format(instrument)
    #
    #             SQL_STATEMENT_SELL = ("SELECT deal_price, deal_quantity  FROM deal "
    #                                   "WHERE deal_type = 'S' "
    #                                   "  deal_instrument_id = {} ").format(instrument)
    #
    #             buy_deals = self.cursor.execute(SQL_STATEMENT_BUY)
    #             sell_deals = self.cursor.execute(SQL_STATEMENT_SELL)
    #             buys = np.array(buy_deals)
    #             sells = np.array(sell_deals)
    #
    #         N_bought = buys.sum(axis=0)[1]
    #         N_sold = sells.sum(axis=0)[1]
    #
    def calcEndPosition(self):
        end_position_list = []
        try:
            cnx = db.get_connection()
            cursor = cnx.cursor()
            for counterparty_name, counterparty_id in counterparty_dict.items():
                position_dict = {'cpty_name':counterparty_name}
                for instrument_name, instrument_id in instrument_dict.items():
                    SQL_STATEMENT_BUY = ("SELECT SUM(deal_quantity) FROM deal "
                                         "WHERE deal_type = 'B' AND "
                                         "deal_instrument_id = {} AND deal_counterparty_id = {}").format(instrument_id, counterparty_id)
                    SQL_STATEMENT_SELL = ("SELECT SUM(deal_quantity) FROM deal "
                                         "WHERE deal_type = 'S' AND "
                                         "deal_instrument_id = {} AND deal_counterparty_id = {}").format(instrument_id, counterparty_id)
                    cursor.execute(SQL_STATEMENT_BUY)
                    result = cursor.fetchone()
                    sum_of_buys = result[0]
                    if sum_of_buys is None:
                        sum_of_buys = 0
                    cursor.execute(SQL_STATEMENT_SELL)
                    result1 = cursor.fetchone()
                    sum_of_sells = result1[0]
                    if sum_of_sells is None:
                        sum_of_sells = 0
                    position_dict[instrument_name] = float(sum_of_buys - sum_of_sells)
                    #        also calculate cash?
                end_position_list.append(position_dict)
            cnx.commit()
            cursor.close()
            return end_position_list
        #       return list of maps
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()