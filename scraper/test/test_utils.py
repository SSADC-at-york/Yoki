# pylint: skip-file

from helper.utils import Utils

util = Utils()

def test_extract_time():
    example_hour1 = "We're currently open.Today's Hours: 8:00 am - 11:00 am"
    assert util.extract_time(example_hour1) == [
        '08:00', '11:00'], "Time Extraction Failed"

def test_shop_closed():
    example_hour1 = "We're currently closed."
    assert util.extract_time(example_hour1) is None, "Failed to see if shop is closed"


def test_extract_shop_name_1():
    data = "William Small Centre (Building 15 on map)"
    assert util.extract_shop_name(
        data) == "William Small Centre", "Couldn't extract shop name"

def test_extract_shop_name_2():
    data = "York Lanes (Building 24 on map)"
    assert util.extract_shop_name(
        data) == "York Lanes", "Couldn't extract shop name"