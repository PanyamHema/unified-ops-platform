#!/usr/bin/env python3
from pymisp import ExpandedPyMISP
from elasticsearch import Elasticsearch

MISP_URL, MISP_KEY = "https://misp.local", "YOUR_KEY"
misp = ExpandedPyMISP(MISP_URL, MISP_KEY, ssl=False)
es = Elasticsearch("http://localhost:9200")

def pull_iocs():
    events = misp.list_events(return_format="json")
    for evt in events:
        for att in evt.get("Attribute", []):
            doc = {
              "ioc": att["value"],
              "type": att["type"],
              "event": evt["Event"]["id"],
              "@timestamp": evt["Event"]["date"]
            }
            es.index(index="threat-intel", body=doc)
            print("Indexed IOC:", att["value"])

if __name__=="__main__":
    pull_iocs()
