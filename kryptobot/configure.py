import json


def load_config(config):

    conf = {
        "db": {
            "engine": "sqlite",
            "name": "core.db",
            "username": None,
            "password": None,
            "host": None
        },
        "apis": {
            "cryptopia": {
                "key": "key",
                "secret": "secret"
            },
            "bittrex": {
                "key": "key",
                "secret": "secret"
            },
            "hitbtc": {
                "key": "key",
                "secret": "secret"
            },
            "binance": {
                "key": "key",
                "secret": "secret"
            }
        },
        "portfolio": {
             "name": "default"
         }
    }

    if isinstance(config, str):
        with open(config, 'r') as f:
            conf = json.load(f)
    elif config:
        conf = config
    return conf
