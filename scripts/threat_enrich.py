#!/usr/bin/env python3
import requests

ABUSEIPDB_KEY = "YOUR_KEY"
VT_KEY = "YOUR_KEY"

def enrich_ip(ip):
    abuse = requests.get(
      f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}",
      headers={"Key":ABUSEIPDB_KEY,"Accept":"application/json"}
    ).json()
    vt = requests.get(
      f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
      headers={"x-apikey":VT_KEY}
    ).json()
    return {
      "abuse_confidence": abuse["data"]["abuseConfidenceScore"],
      "vt_malicious": vt["data"]["attributes"]["last_analysis_stats"]["malicious"]
    }
