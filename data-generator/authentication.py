import sys
import db

def is_user_authenticated(username, password):
    is_auth = False
    try:
        cnx = db.get_connection()
        cursor = cnx.cursor()
        get_password = ("SELECT user_pwd FROM users "
                          "WHERE user_id = %s")
        data_user = (username,)
        cursor.execute(get_password, data_user)
        result = cursor.fetchone()

        if result[0] == password:
            is_auth = True

        cnx.commit()
        cursor.close()
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        print()
    return is_auth
