import os
import json
import sys


def get_account_data():
    """
    Read account data from separate json file
    :return: None
    """
    try:
        with open(Config.ACCOUNT_DATA, 'r', encoding='utf-8') as r_file:
            data = json.load(r_file)
            Config.USERNAME = data['username']
            Config.PASSWORD = data['password']
    except FileNotFoundError:
        print(f'Cannot find account config file "{Config.ACCOUNT_DATA}". Exit.')
        sys.exit(2)
    except json.decoder.JSONDecodeError:
        print(f'"{Config.ACCOUNT_DATA}" config file is incorrect json file. Exit.')
        sys.exit(3)


class Config:
    USERNAME = ''
    PASSWORD = ''
    CHROME_PATH = os.path.join(os.path.dirname(__file__), 'tools', 'chromedriver.exe')
    DATA_DIR = 'data'
    ACCOUNT_DATA = os.path.join(os.path.dirname(__file__), 'account_details.json')


get_account_data()

