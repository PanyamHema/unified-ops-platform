#!/usr/bin/env python3
import requests

SLACK_WEBHOOK = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
TEAMS_WEBHOOK = "https://outlook.office.com/webhook/AAA/BBB"

def send_slack(msg):
    requests.post(SLACK_WEBHOOK, json={"text":msg})

def send_teams(msg):
    requests.post(TEAMS_WEBHOOK, json={"text":msg})

if __name__=="__main__":
    send_slack("Unified Ops Platform is online.")
    send_teams("Unified Ops Platform is online.")
