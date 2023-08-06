import requests
import pandas as pd
import json
from config import *

def get_all_energy_solutions(token, BASE_URL=BASE):
    BASE_URL = BASE_URL + "/energy_solutions"

    response = requests.get(BASE_URL, headers={"Authorization":token})

    df = pd.json_normalize(response.json())
    return df


def enter_new_energy_solution(token, args, BASE_URL=BASE):
    print(args)
    BASE_URL = BASE_URL + "/energy_solutions"

    #converts py dict to json with indent = 4 and sends it to the url in a post request
    response = requests.post(BASE_URL, json.dumps(args, indent = 4), headers={"Authorization":token})
    print(response.json())
    return response.json()
