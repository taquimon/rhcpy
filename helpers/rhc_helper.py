import json
from config.config import abs_path
def read_json_file(club_name):
    
    with open(f"{abs_path}/resources/data.json") as json_file:
        data = json.load(json_file)
    
    return data