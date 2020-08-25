 import db
 import numpy as np
 import json
 
 
 class MetricsCalculator:
    def __init__(self):
        try:
            self.cnx = db.get_connection()
            self.cursor = cnx.cursor()
             
        except:
               print("Oops!", sys.exc_info()[0], "occurred.")
               print()
               
               
    def calcAvgInstrumentPrice(self,instrument, start, stop):
        try:
        
            SQL_STATEMENT_BUY = ("SELECT AVG(price) FROM deals"
                            "WHERE deal_type = 'B' AND"
                            "deal_time BETWEEN {} AND {} AND"
                            "deal_instrument_id =(SELECT instrument_id FROM instruments WHERE  instrument_name = {}").format(start, stop, instrument))
            SQL_STATEMENT_SELL = ("SELECT AVG(price) FROM deals"
                            "WHERE deal_type = 'S' AND"
                            "deal_time BETWEEN {} AND {} AND"
                            "deal_instrument_id =(SELECT instrument_id FROM instruments WHERE  instrument_name = {}").format(start, stop, instrument))
                            
            avg_buy_price  = self.cursor.execute(SQL_STATEMENT_BUY)
            avg_sell_price  = self.cursor.execute(SQL_STATEMENT_SELL)
            return avg_buy_price, avg_sell_price
            
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
    
    
    def calcRealizedProfit(self):
        RealizedProfit = 0.
        try:
        
            for instrument in instruments:
                SQL_STATEMENT_BUY = ("SELECT deal_price, deal_quantity FROM deal"
                                 "WHERE deal_type = 'B' "
                                " deal_instrument_id =(SELECT instrument_id FROM instruments WHERE  instrument_name = {}").format(instrument)
                                
                
                SQL_STATEMENT_SELL = ("SELECT deal_price, deal_quantity  FROM deal"
                                 "WHERE deal_type = 'S' "
                                "  deal_instrument_id =(SELECT instrument_id FROM instruments WHERE  instrument_name = {}").format(instrument)
                
                
                                
                buy_deals = self.cursor.execute(SQL_STATEMENT_BUY)
                sell_deals = self.cursor.execute(SQL_STATEMENT_SELL)
                buys  = np.array(buy_deals)
                sells = np.array(sell_deals)
                
                
                N_bought = buys.sum(axis = 0)[1]
                N_sold = sells.sum(axis = 0)[1]
                
                if (N_bought<N_sold):
                    raise Exception("You can't sell more assets than you have!!!")
                    
                    
                cash_earned= sum([x*y for x, y in zip(sells[:, 1], sells[:, 0])])
                instrument_profit = cash_earned
                
                for price, quantity in buys :
                    if N_sold>0:
                        if N_sold> quantity:
                            instrument_profit -= quantity*price
                            N_sold -= quantity
                            N_bought -= quantity
    
                        else:
                            instrument_profit -= N_sold*price
                            N_sold -= N_sold
                            N_bought -= N_sold
                    
                RealizedProfit+=instrument_profit
            return RealizedProfit
                    
            
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()
            
        
        
    def calcEffectiveProfit(self):
        
        RealizedProfit = 0.
        EffectiveProfit = 0.
        remaining_assets =[]
            try:
            
                for instrument in instruments:
                    SQL_STATEMENT_BUY = ("SELECT deal_price, deal_quantity FROM deal"
                                     "WHERE deal_type = 'B' "
                                    " deal_instrument_id =(SELECT instrument_id FROM instruments WHERE  instrument_name = {}").format(instrument)
                                    
                    
                    SQL_STATEMENT_SELL = ("SELECT deal_price, deal_quantity  FROM deal"
                                     "WHERE deal_type = 'S' "
                                    "  deal_instrument_id =(SELECT instrument_id FROM instruments WHERE  instrument_name = {}").format(instrument)
                    
                    
                                    
                    buy_deals = self.cursor.execute(SQL_STATEMENT_BUY)
                    sell_deals = self.cursor.execute(SQL_STATEMENT_SELL)
                    buys  = np.array(buy_deals)
                    sells = np.array(sell_deals)
                    
                    
                    N_bought = buys.sum(axis = 0)[1]
                    N_sold = sells.sum(axis = 0)[1]
                    
                    if (N_bought<N_sold):
                        raise Exception("You can't sell more assets than yoy have!!!")
                        
                        
                    cash_earned= sum([x*y for x, y in zip(sells[:, 1], sells[:, 0])])
                    instrument_profit = cash_earned
                    
                    for price, quantity in buys :
                        if N_sold>0:
                            if N_sold> quantity:
                                instrument_profit -= quantity*price
                                N_sold -= quantity
                                N_bought -= quantity
        
                            else:
                                instrument_profit -= N_sold*price
                                N_sold -= N_sold
                                N_bought -= N_sold
                    
                    RealizedProfit+=instrument_profit
                    remaining_assets.append(N_bought)
                SQL_STATEMENT_FRESH_PRICES =("SELECT deal_price FROM deal"
                                            "WHERE deal_id IN (SELECT MAX(deal_id) FROM deal GROUP BY instrument_id)
                                            "G").format(instrument)
                fresh_prices = self.cursor.execute(SQL_STATEMENT_FRESH_PRICES)
                EffectiveProfit = RealizedProfit + sum([x*y for x, y in zip(remaining_assets, fresh_prices]))
        
        
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()


    def calcEndPosition(self):
        
        try:
            
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print()




