import json

import requests

SERVER_LIST_URL = 'http://47.241.186.78/server.txt'
CREATE_ACCOUNT_URL = 'http://47.241.186.78/userinfo/userinfo_insert.php?userId={}&pass={}'
UPDATE_ACCOUNT_URL = 'http://47.241.186.78/userinfo/update.php?userId={}&password={}&oldpass={}'


def server_list_request():
    response = requests.get(SERVER_LIST_URL)
    response.encoding = "utf-8"
    ret_text = response.text
    return ret_text

def create_account_request(account, password):
    response = requests.get(CREATE_ACCOUNT_URL.format(account, password))
    response.encoding = "utf-8"
    ret_dict = json.loads(response.text)
    return ret_dict

def update_account_request(account, new_password, old_password):
    response = requests.get(UPDATE_ACCOUNT_URL.format(account, new_password, old_password))
    response.encoding = "utf-8"
    ret_dict = json.loads(response.text)
    return ret_dict