#!/usr/bin/env python3
import xmlrpc.client, subprocess, json

# OpenVAS Manager RPC
OM = xmlrpc.client.ServerProxy("https://127.0.0.1:9390")
USER, PASS = "admin", "admin"

def run_scan(target_name, target_ip):
    OM.authenticate(USER, PASS)
    target_id = OM.get_target_id_by_name(USER, PASS, target_name)
    task_id = OM.create_task(USER,PASS,"scan_"+target_name,target_id)
    OM.start_task(USER,PASS,task_id)
    return task_id

def fetch_report(task_id):
    report_id = OM.get_task_report_id(USER,PASS,task_id)
    report = OM.get_report(USER,PASS,report_id, format_id="JSON")
    return json.loads(report)

def remediate(report):
    hosts = [h["host"] for vuln in report["results"] for h in [vuln["target"]]]
    for host in set(hosts):
        subprocess.run(["ansible-playbook","remediate.yml","-l",host])

if __name__=="__main__":
    tid = run_scan("HQ-NET","10.1.1.0/24")
    print("Scan started:", tid)
    # ... wait or poll until done ...
    rpt = fetch_report(tid)
    remediate(rpt)
