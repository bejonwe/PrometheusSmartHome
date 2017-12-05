"""
Fills Prometheus with Smart Home Data
"""

from datetime import datetime
import time
import os
import configparser
import importlib

from apscheduler.schedulers.background import BackgroundScheduler
from prometheus_client import start_http_server

if __name__ == '__main__':
    scheduler = BackgroundScheduler()

    config = configparser.ConfigParser()
    config.read("config.ini")
    for moduleName in config.sections():
        if config[moduleName]['enabled'] == 'yes':
            print("Modul " + moduleName + " enabled!")
            module = importlib.import_module("."+moduleName,"modules")
            if "getdata" in dir(module) and "init" in dir(module):
                module.init(config[moduleName])
                scheduler.add_job(module.getdata, 'interval', seconds=int(config[moduleName]['interval']))
            else:
                print("Module " + moduleName + " has no function getdata or init!")

    scheduler.start()
    start_http_server(8000)
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
