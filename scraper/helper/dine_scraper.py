"""
Scraper module which sends get request to youku food service servers and extracts
Data from the response, and returns it as a dictionary.
"""

import datetime
import sys
from typing import List

import bs4
import requests

if __name__ == "__main__":
    import utils
    yutil = utils.Utils()
else:
    from helper import utils
    yutil = utils.Utils()


class Extractor:
    """
    Extracts the dining directory and returns a dictionary containing the data
    """

    def __init__(self):
        self.current_error = None

    def dining_dir(self) -> List:
        """
        Returns a list of dictionaries containing the dining directory
        """
        json_data = {
            "last_updated": None,
            "data": []
        }

        url = "https://www.yorku.ca/foodservices/dining-directory/"

        data_model = {
            "isOpen": False,
            "name": None,
            "hours": None,
            "address": None,
            "map_address": None,
        }

        # Get the page
        response = requests.get(url)

        if response.status_code != 200:
            current_error = "Could not get page"
            print(current_error)
            sys.exit(1)

        # create soup
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # get table
        table = soup.find("table")

        # get rows
        rows = table.find_all("tr")

        #  extract data
        for row in rows:
            # get columns
            columns = row.find_all("td")

            if len(columns) > 1:
                name = columns[0].find("a").text
                # extract hours
                hours = columns[1].find(
                    "div", {"class": "op-is-open-shortcode"}).text
                # extract address
                address = columns[2].text

                if yutil.extract_time(hours) is not None:
                    data_model["hours"] = yutil.extract_time(hours)
                    data_model["isOpen"] = True

                data_model["name"] = name
                data_model["address"] = yutil.extract_shop_name(address)
                data_model["map_address"] = yutil.extract_shop_address(address)

                json_data["data"].append(data_model.copy())

        json_data["last_updated"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        return json_data
