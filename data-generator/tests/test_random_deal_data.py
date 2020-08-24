import ast
import json
import sys

import db
from random_deal_data import RandomDealData


def test_random_deal_is_saved():
    is_saved = False
    randomDeal = RandomDealData()
    instruments = randomDeal.createInstrumentList()
    json_data = randomDeal.createRandomData(instruments)
    data = ast.literal_eval(json_data)
    deal_id = data['id']
    try:
        cnx = db.get_connection()
        cursor = cnx.cursor()
        get_deal = ("SELECT deal_time, deal_counterparty_id, deal_type, deal_price, deal_quantity FROM deal "
                    "WHERE deal_id = %s")
        data_deal = (deal_id,)
        cursor.execute(get_deal, data_deal)
        result = cursor.fetchone()

        if result is not None:
            is_saved = True

        cnx.commit()
        cursor.close()
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        print()
    assert is_saved is True


if __name__ == "__main__":
    test_random_deal_is_saved()
