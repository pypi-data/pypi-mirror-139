import requests
import json
from config import *

def get_token(UoE_id, password, BASE_URL=BASE):
    BASE_URL = BASE_URL + "/login"

    data = {"username": UoE_id, "password":password}

    response = requests.post(BASE_URL, data=data)
    token = response.json()

    reformatted_token = token['token_type'] + " " + token["access_token"]

    print("Login Sucessful.")
    print(reformatted_token)
    return reformatted_token
