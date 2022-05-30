"""
Main file which runs the program.
"""

import json

from helper.dine_scraper import Extractor

extractor = Extractor()
dining = extractor.dining_dir()

with open("data/dining/dining.json", "w", encoding="utf-8") as outfile:
    json.dump(dining, outfile, indent=2)
