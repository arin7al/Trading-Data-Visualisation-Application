import authentication


def test_correct_user_should_return_true():
    user = "john"
    password = "gradprog2016@03"

    result = authentication.is_user_authenticated(user, password)
    assert result is True

def test_incorrect_user_should_return_false():
    user = "john"
    password = "incorrect"

    result = authentication.is_user_authenticated(user, password)
    assert result is False


if __name__ == "__main__":
    test_correct_user_should_return_true()
    test_incorrect_user_should_return_false()
