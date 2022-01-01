"""
Main file which runs the program.
Imports helper functions from helper folder
"""

import json
from helper.scraper import Extractor


extractor = Extractor()
dining = extractor.dining_dir()

with open("data/dining.json", "w", encoding="utf-8") as outfile:
    json.dump(dining, outfile, indent=2)
