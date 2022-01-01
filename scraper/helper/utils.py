"""
Utility file containing helper functions, error handling, etc.
"""

import regex as re
import datetime


class Error(Exception):
    """Base class for other exceptions"""


class TimeExtractError(Error):
    """Raised when time couldn't be extraced from the sentences"""


class ShopNameExtractError(Error):
    """Raised when shop name couldn't be extraced from the sentences"""


class Utils:
    """
    Helper functions class
    """
    CLOSED = "We're currently closed."

    def __init__(self):
        """
        init method
        does nothing for now
        """

    def extract_time_from_word(self, word):
        """
        takes in a datetime in as "natural" word
        returns a datetime object
        """
        time_object = datetime.datetime.strptime(word, '%I:%M %p')
        time_string = time_object.strftime('%H:%M')
        return time_string

    def extract_time(self, sentence):
        """
        extract open and close time from a sentence
        if the sentence is not a time, raise RegExMatchFailed
        if the sentence is a time, return a tuple of open and close time
        if the shop is closed, return None
        """

        if sentence == self.CLOSED:
            return None

        # extract hours with am/pm
        hours = re.findall(r'[0-9]{1,2}:[0-9]{2} \w\w', sentence)

        if hours:
            if len(hours) == 2:
                return [
                    self.extract_time_from_word(hours[0]),
                    self.extract_time_from_word(hours[1])
                    ]
            raise TimeExtractError(
                "Couldn't extract the passed time obj is bad", hours)
        raise TimeExtractError("Couldn't extract hours from the sentence")

    def extract_shop_name(self, sentence):
        """
        extract shop name from a sentence
        """
        # extract shop name which is everything except stuff in parantheses
        shop_name = re.findall(r'[^\(]*', sentence)

        if shop_name:
            return shop_name[0].strip()

        raise ShopNameExtractError(
            "Couldn't extract shop name from the sentence")

    def extract_shop_address(self, sentence):
        """
        extract shop map address from a sentence
        """
        # extract shop name which is in parantheses and remove extra junk!
        shop_address = re.findall(r'\(.*\)', sentence)
        if shop_address:
            shop_address = shop_address[0].replace(
                '(', '').replace(')', '').replace(' on map', '').strip()
            return shop_address
        return None
