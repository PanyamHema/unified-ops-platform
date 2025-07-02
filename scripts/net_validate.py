#!/usr/bin/env python3
import yaml
from netmiko import ConnectHandler

with open("expected_states.yml") as f:
    expected = yaml.safe_load(f)

for host, cfg in expected.items():
    conn = ConnectHandler(**cfg["conn"])
    for cmd, exp in cfg["checks"].items():
        out = conn.send_command(cmd)
        print(f"{host}: {cmd} → {'OK' if exp in out else 'FAIL'}")
    conn.disconnect()
