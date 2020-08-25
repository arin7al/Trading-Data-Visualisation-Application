from db import get_all_deals, get_connection, is_connection_open, close_connection


def test_opened_connection_is_open():
    get_connection()
    assert is_connection_open() is True


def test_closed_connection_is_closed():
    close_connection()
    assert is_connection_open() is False


def test_get_all_deals():
    result = get_all_deals()
    print(result)
    assert result is not None


if __name__ == "__main__":
    test_opened_connection_is_open()
    test_closed_connection_is_closed()
    test_get_all_deals()
