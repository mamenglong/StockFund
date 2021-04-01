import json
import os
import threading

from stock.Stock import Stock

global config
global userAgents


def __init__():
    path = os.path.dirname(__file__)
    print(path)
    with open("../config/config.json", "r+", encoding="utf-8") as f:
        global config
        config = json.loads(f.read())
    with open("../config/user_agents.txt", "r+", encoding="utf-8") as f:
        global userAgents
        userAgents = f.read().split('\n')
    run()


def run():
    stock = Stock(config["stock"], userAgents)
    stock.run()


if __name__ == '__main__':
    __init__()
    pass
