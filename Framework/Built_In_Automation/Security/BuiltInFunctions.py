import os
import subprocess
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from arachni_download import check_and_install_arachni
from arachni_run import run_arachni_scan, generate_report_from_afr

def port_scaning_nmap(data_set: list) -> str:
    target = next(item[2] for item in data_set if item[0] == 'target')
    nmap_action = next(item[2] for item in data_set if item[0] == 'nmap')
    command = ["nmap", nmap_action, target]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Command Output:", result.stdout)
        return "passed"
    except subprocess.CalledProcessError as e:
        print("An error occurred while running nmap:")
        print(e.stderr)
        return "zeuz_failed"

def server_scaning_wapiti(data_set: list) -> str:
    target = next(item[2] for item in data_set if item[0] == 'target')
    wapiti_action = next(item[2] for item in data_set if item[0] == 'wapiti')
    if not target.startswith(("http://", "https://")):
        target = "http://" + target
    command = ["wapiti", wapiti_action, "-u", target]

    try:
        print(command)
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Command Output:", result.stdout)
        return "passed"
    except subprocess.CalledProcessError as e:
        print("An error occurred while running wapiti:")
        print(e.stderr)
        return "zeuz_failed"

def server_scaning_arachni(data_set: list) -> str:
    arachni_target = next(item[2] for item in data_set if item[0] == 'arachni')
    success = check_and_install_arachni()
    if success:
        if not arachni_target.startswith(("http://", "https://")):
            arachni_target = "http://" + arachni_target
        run_arachni_scan(arachni_target)
        generate_report_from_afr()
        return "passed"
    else:
        print("***** Arachni setup failed. *****")
        return "zeuz_failed"