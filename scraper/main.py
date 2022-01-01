import json
from helper.scraper import Extractor


extractor = Extractor()
dining = extractor.dining_dir()

with open("data/dining.json", "w") as outfile:
    json.dump(dining, outfile, indent=2)