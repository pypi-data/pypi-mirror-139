import requests
import pandas as pd
import json
from config import *

def get_all_lysate_systems(token, BASE_URL=BASE):
    BASE_URL = BASE_URL + "/lysate_systems"

    response = requests.get(BASE_URL, headers={"Authorization":token})

    df = pd.json_normalize(response.json())
    return df




def create_new_lysate_system(token, args, BASE_URL=BASE):
    BASE_URL = BASE_URL + "/lysate_systems"

    response = requests.post(BASE_URL, json.dumps(args, indent = 4) , headers={"Authorization":token})

    print(response.json())
    return response.json()
