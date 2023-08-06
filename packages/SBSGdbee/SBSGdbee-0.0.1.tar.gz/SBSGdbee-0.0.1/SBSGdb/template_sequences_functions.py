import requests
import pandas as pd
import json
from config import *

def get_all_template_sequences(token, BASE_URL=BASE):
    BASE_URL = BASE_URL + "/template_sequences"

    response = requests.get(BASE_URL, headers={"Authorization":token})

    df = pd.json_normalize(response.json())
    return df




def enter_new_template_sequence(token, args, BASE_URL=BASE):
    BASE_URL = BASE_URL + "/template_sequences"

    response = requests.post(BASE_URL, json.dumps(args, indent = 4) , headers={"Authorization":token})
    print(response.json())
    return response.json()
