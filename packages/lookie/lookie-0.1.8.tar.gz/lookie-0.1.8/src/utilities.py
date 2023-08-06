import datetime
import logging
import sys
import json
import os


def date_time_now():
    to_return = datetime.datetime.utcnow().isoformat()
    return to_return


def display(message):
    logging.log(level=1, msg=message)
    to_print = f"{date_time_now()}\t{message}"
    print(to_print)
    return True


def get_path():
    default_path = str(os.getcwd())
    display(message=default_path)
    return default_path


def config_reader():
    with open(file=get_path() + "gaze.config.json", mode='r') as cf:
        gaze_config = json.load(cf)
        return gaze_config
