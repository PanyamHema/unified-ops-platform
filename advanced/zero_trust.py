#!/usr/bin/env python3
import requests
from netmiko import ConnectHandler

ES_URL="http://localhost:9200/risk-scores/_search"

def get_high_risk():
    q={"query":{"range":{"score":{"gte":70}}}}
    hits=requests.get(ES_URL,json=q).json()["hits"]["hits"]
    return [h["_source"]["ip"] for h in hits]

def quarantine(ip):
    dev={"device_type":"cisco_ios","host":"203.0.113.1","username":"admin","password":"StrongP@ss"}
    conn=ConnectHandler(**dev)
    cmds=[f"interface GigabitEthernet1/0/1","description Quarantine {ip}","switchport access vlan 999","exit",
          "vlan 999","name QUARANTINE","exit"]
    conn.send_config_set(cmds); conn.disconnect()
    print("Quarantined", ip)

if __name__=="__main__":
    for ip in get_high_risk():
        quarantine(ip)
