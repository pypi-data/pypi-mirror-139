import http.client
import json
import os
import time
from urllib.parse import urlparse
from src.utilities import display, config_reader


def send_message_to_slack(message):
    slack_config = config_reader().get("slack")
    slack_url = urlparse(slack_config.get("ecs-cluster-alert").get("hook"))

    conn = http.client.HTTPSConnection(slack_url.netloc)

    the_data = {
        "channel": slack_config.get("ecs-cluster-alert").get("channel"),
        "text": message
    }

    headers = {'Content-Type': "application/json"}

    conn.request("POST", slack_url.path, json.dumps(the_data), headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def check_ping(hostname):
    """Check ping response of a host or IP."""
    response = os.system("ping -c 1 -t 1 " + hostname + "> /dev/null 2>&1")

    if response == 0:
        pingstatus = 1
    else:
        pingstatus = 0

    return pingstatus


def ping_test(args):
    hostname = args.hostname
    surname = args.surname
    how_many_check = args.count
    interval = args.interval

    counter = 0

    for _ in range(how_many_check):
        ping_response = check_ping(hostname=hostname)
        counter += ping_response
        time.sleep(interval)

    percentage = 100 - int((counter / how_many_check) * 100)

    if percentage >= 50:

        message = f"""Ping check to *'{surname}/{hostname}'* is marked as *'failed'*
as *{percentage}%* checks are failed."""
        display(message=message)
    else:
        message = f"Passed more than 50% of the ping test to: {surname}/{hostname}."
        display(message=message)


def string_check(args):
    url = args.url
    string = args.string

    parsed_url = urlparse(url=url)

    domain = parsed_url.netloc
    scheme = parsed_url.scheme
    path = parsed_url.path

    if "https" in scheme.lower():
        conn = http.client.HTTPSConnection(domain)
    else:
        conn = http.client.HTTPConnection(domain)

    payload = ""

    headers = {
        'Content-Type': "application/json",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }

    conn.request("GET", path, payload, headers=headers)

    res = conn.getresponse()

    message = f"Found '{string}' at {url}"

    if res.status == 200:
        data = res.read()
        if string.lower() in data.decode("utf-8").lower():
            display(message=message)
            return True
        else:
            display(message=message.replace("Found", "Not Found"))
            return False
    else:
        message = f"Error accessing {url}"
        display(display(message=message))
        return False