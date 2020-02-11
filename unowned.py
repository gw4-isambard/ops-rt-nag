#!/usr/bin/env python3

import rt
import configparser
import requests
import json

config = configparser.RawConfigParser()
config.read("example.cfg")
url = config.get("RT Server", "url")
path = config.get("RT Server", "path")
username = config.get("RT Server", "user_login")
password = config.get("RT Server", "user_pass")
webhook = config.get("Slack", "webhook")

tracker = rt.Rt(url + path, username, password)
tracker.login()
unowned_query = "Owner = 'Nobody' AND Status = '__Active__'"
tickets = tracker.search(
    Queue=rt.ALL_QUEUES, order="Status", raw_query=unowned_query, Format="s"
)
if tickets:
    message = f"There are currently {len(tickets)} unowned tickets:\n"
    for ticket in tickets:
        message += f"- <{url}Ticket/Display.html?id={ticket['numerical_id']}|{ticket['numerical_id']} - {ticket['Subject']}>\n"
    payload = {"text": message}
    headers = {"content-type": "application/json"}
    slack = requests.post(webhook, data=json.dumps(payload), headers=headers)
