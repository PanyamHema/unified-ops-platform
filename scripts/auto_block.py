#!/usr/bin/env python3
import json, requests, time
from netmiko import ConnectHandler

ELASTIC_URL = "http://localhost:9200/suricata-*/_search"
SLACK_WEBHOOK = "https://hooks.slack.com/services/XXX/YYY/ZZZ"

def fetch_critical_alerts():
    q = {"query":{"match":{"alert.signature":"Potential Reconnaissance"}}}
    resp = requests.get(ELASTIC_URL, headers={"Content-Type":"application/json"}, json=q)
    hits = resp.json()["hits"]["hits"]
    return {h["_source"]["src_ip"] for h in hits}

def push_acl_block(ip):
    device = {"device_type":"cisco_ios","host":"203.0.113.1",
              "username":"admin","password":"StrongP@ss","secret":"StrongP@ss"}
    conn = ConnectHandler(**device); conn.enable()
    cmds = [f"ip access-list extended BLOCKED_IPS","deny ip host {ip} any","exit"]
    conn.send_config_set(cmds); conn.save_config(); conn.disconnect()

def notify_slack(ip):
    requests.post(SLACK_WEBHOOK, json={"text":f"Blocked {ip}"})

if __name__=="__main__":
    while True:
        for ip in fetch_critical_alerts():
            push_acl_block(ip); notify_slack(ip)
        time.sleep(300)
