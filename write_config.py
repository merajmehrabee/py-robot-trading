# python 3.x
from configparser import ConfigParser

config = ConfigParser()

config.add_section('main')
config.set('main', 'CLIENT_ID','')
config.set('main', 'REDIRECT_URI', '')
config.sett('main', 'JSON_PATH', '')
config.sett('main', 'ACCOUNT_NUMBER', '')

with open('configs/config.ini', 'w+') as f:
    config.write(f)