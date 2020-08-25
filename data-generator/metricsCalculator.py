import db
import numpy as np
import sys

instruments = ['Astronomica','Borealis','Celestial','Deuteronic','Eclipse',
               'Floral','Galactia','Heliosphere','Interstella','Jupiter',
               'Koronis','Lunatic']

class MetricsCalculator:
    def __init__(self):
        try:
            self.cnx = db.get_connection()
            self.cursor = self.cnx.cursor()

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()

    def calcAvgInstrumentPrice(self, instrument, start, stop):
        try:
            SQL_STATEMENT_BUY = ("SELECT AVG(deal_price) FROM deal "
                                 "WHERE deal_type = 'B' AND "
                                 "deal_time BETWEEN {} AND {} AND "
                                 "deal_instrument_id =(SELECT instrument_id "
                                 "FROM instrument WHERE instrument_name = {} ").format(start, stop, instrument)
            SQL_STATEMENT_SELL = ("SELECT AVG(deal_price) FROM deal "
            "WHERE deal_type = 'S' AND "
            "deal_time BETWEEN {} AND {} AND "
            "deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = {} ").format(start,
                                                                                                             stop,
                                                                                                             instrument)

            self.cursor.execute(SQL_STATEMENT_BUY)
            result = self.cursor.fetchone()
            self.cursor.execute(SQL_STATEMENT_SELL)
            result2 = self.cursor.fetchone()
            return result[0], result2[0]

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
            return None, None

    def calcRealizedProfit(self):
        RealizedProfit = 0.

        try:
            SQL_STATEMENT_DEAL_IDS = ("SELECT DISTINCT deal_instrument_id FROM deal ")
            self.cursor.execute(SQL_STATEMENT_DEAL_IDS)
            instruments_ids = self.cursor.fetchall()
            print(type(instruments_ids), instruments_ids)
            for instrument in instruments_ids:
                SQL_STATEMENT_BUY = ("SELECT deal_price, deal_quantity FROM deal "
                                     "WHERE deal_type = 'B' AND"
                                     " deal_instrument_id = {} ").format(instrument[0])

                SQL_STATEMENT_SELL = ("SELECT deal_price, deal_quantity  FROM deal "
                                      "WHERE deal_type = 'S' AND"
                                      "  deal_instrument_id = {} ").format(instrument[0])

                try:
                    self.cursor.execute(SQL_STATEMENT_BUY)
                    buy_deals = self.cursor.fetchall()
                    print(buy_deals)
                    buys = np.array(buy_deals[0])
                    N_bought = buys.sum(axis=0)[1]
                except:
                    N_bought = 0
                try:
                    self.cursor.execute(SQL_STATEMENT_SELL)
                    sell_deals = self.cursor.fetchall()
                    print(sell_deals)
                    sells = np.array(sell_deals[0])
                    N_sold = sells.sum(axis=0)[1]
                except:
                    N_sold = 0

                print(N_bought, N_sold)


                if N_bought < N_sold:
                    raise Exception("You can't sell more assets than you have!!!")

                cash_earned = sum([x * y for x, y in zip(sells[:, 1], sells[:, 0])])
                instrument_profit = cash_earned

                for price, quantity in buys:
                    if N_sold > 0:
                        if N_sold > quantity:
                            instrument_profit -= quantity * price
                            N_sold -= quantity
                            N_bought -= quantity

                        else:
                            instrument_profit -= N_sold * price
                            N_sold -= N_sold
                            N_bought -= N_sold

                RealizedProfit += instrument_profit
            return RealizedProfit


        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
            return None


    def calcEffectiveProfit(self):
        RealizedProfit = 0.
        EffectiveProfit = 0.
        remaining_assets = []
        try:

            for instrument in instruments:
                SQL_STATEMENT_BUY = ("SELECT deal_price, deal_quantity FROM deal "
                                     "WHERE deal_type = 'B' "
                                     " deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = {} ").format(
                    instrument)

                SQL_STATEMENT_SELL = ("SELECT deal_price, deal_quantity  FROM deal "
                                      "WHERE deal_type = 'S' "
                                      "  deal_instrument_id =(SELECT instrument_id FROM instrument WHERE  instrument_name = {} ").format(
                    instrument)

                self.cursor.execute(SQL_STATEMENT_BUY)
                buy_deals = self.cursor.fetchone()
                self.cursor.execute(SQL_STATEMENT_SELL)
                sell_deals = self.cursor.fetchone()
                buys = np.array(buy_deals[0])
                sells = np.array(sell_deals[0])

                N_bought = buys.sum(axis=0)[1]
                N_sold = sells.sum(axis=0)[1]

                if N_bought < N_sold:
                    raise Exception("You can't sell more assets than yoy have!!!")

                cash_earned = sum([x * y for x, y in zip(sells[:, 1], sells[:, 0])])
                instrument_profit = cash_earned

                for price, quantity in buys:
                    if N_sold > 0:
                        if N_sold > quantity:
                            instrument_profit -= quantity * price
                            N_sold -= quantity
                            N_bought -= quantity

                        else:
                            instrument_profit -= N_sold * price
                            N_sold -= N_sold
                            N_bought -= N_sold

                RealizedProfit += instrument_profit
                remaining_assets.append(N_bought)
            SQL_STATEMENT_FRESH_PRICES = ("SELECT deal_price FROM deal "
                                          "WHERE deal_id IN (SELECT MAX(deal_id) FROM deal GROUP BY instrument_id) ").format(instrument)
            self.cursor.execute(SQL_STATEMENT_FRESH_PRICES)
            fresh_prices = self.cursor.fetchone()
            EffectiveProfit = RealizedProfit + sum([x * y for x, y in zip(remaining_assets, fresh_prices[0])])


        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
            return None


    #def calcEndPosition(self):
    #    try:

    #    except:
    #        print("Oops!", sys.exc_info()[0], "occurred.")
    #        print()