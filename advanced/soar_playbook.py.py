#!/usr/bin/env python3
from thehive4py.api import TheHiveApi
from thehive4py.models import Case, Alert

API = TheHiveApi("https://thehive.local", "API_KEY")

def create_case(alert_json):
    alert = Alert(**alert_json)
    API.create_alert(alert)
    case = Case(title="Automated Incident", description="Raised via script")
    resp = API.create_case(case)
    print("Case created:", resp.json()["id"])

if __name__=="__main__":
    sample_alert = {
      "title":"Suspicious IP detected",
      "type":"external",
      "source":"elastic",
      "sourceRef":"alert-123",
      "tlp":2
    }
    create_case(sample_alert)
