import os
import subprocess
import shutil
import sys
from urllib.parse import urlparse
from tabulate import tabulate

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from arachni_download import check_and_install_arachni
from arachni_run import run_arachni_scan, generate_report_from_afr
from helper import extract_target, check_perl_installed, display_table, save_report_to_file


def port_scaning_nmap(data_set: list) -> str:
    if not shutil.which("nmap"):
        error_data = [
            ["Error", "nmap is not installed on your system."],
            ["Solution", "Please install it using the following link:"],
            ["Download Link", "https://nmap.org/download.html"],
        ]
        display_table(error_data, headers=["Message", "Details"], title="Nmap Error")
        return "zeuz_failed"

    target_url = next(item[2] for item in data_set if item[0] == "target")
    nmap_action = next(item[2] for item in data_set if item[0] == "nmap")
    target = extract_target(target_url)
    command = ["nmap", nmap_action, target]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_file_path = "/home/antu/Desktop/nmap_scan_result.txt"
        save_report_to_file(result.stdout, output_file_path)

        success_data = [
            ["Command", " ".join(command)],
            ["Output", result.stdout.strip()],
        ]
        display_table(success_data, headers=["Description", "Details"], title="Nmap Scan Result")
        return "passed"
    except subprocess.CalledProcessError as e:
        error_data = [
            ["Command", " ".join(command)],
            ["Error", e.stderr.strip()],
        ]
        display_table(error_data, headers=["Description", "Details"], title="Nmap Error")
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


def server_scaning_nikto(data_set: list) -> str:
    """
    Runs Nikto scan if Perl is installed, otherwise gives installation instructions based on platform.
    """
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
    # Updated path to nikto.pl based on the given location
    NIKTO_DIR = os.path.join(BASE_DIR, "tools", "security", "nikto", "program")
    NIKTO_SCRIPT_PATH = os.path.join(NIKTO_DIR, "nikto.pl")
    # Get the nikto target URL from the data_set
    nikto_target = next(item[2] for item in data_set if item[0] == 'nikto')

    if not check_perl_installed():
        # Perl is not installed, print installation instructions based on platform
        system_platform = sys.platform
        installation_data = []

        if system_platform == "win32":
            installation_data = [
                ["Message", "Perl is not installed on your system."],
                ["Solution", "Install Perl from the following link:"],
                ["Download Link", "https://strawberryperl.com/"]
            ]
            display_table(installation_data, headers=["Message", "Details"], title="Perl Installation (Windows)")
        elif system_platform == "darwin":
            installation_data = [
                ["Message", "Perl is not installed on your system."],
                ["Solution", "Install Perl using Homebrew:"],
                ["Command", "brew install perl"]
            ]
            display_table(installation_data, headers=["Message", "Details"], title="Perl Installation (macOS)")
        else:
            installation_data = [
                ["Message", "Perl is not installed on your system."],
                ["Solution", "Install Perl using your system's package manager:"],
                ["Command", "sudo apt install perl"]
            ]
            display_table(installation_data, headers=["Message", "Details"], title="Perl Installation (Linux)")
        return "zeuz_failed"

    # Check if the nikto.pl file exists at the correct path
    if not os.path.exists(NIKTO_SCRIPT_PATH):
        error_data = [
            ["Error", f"Nikto script (nikto.pl) not found at {NIKTO_SCRIPT_PATH}."],
            ["Solution", "Ensure the script is located at the correct path."],
            ["Action", "Check if the Nikto repository was correctly cloned."]
        ]
        display_table(error_data, headers=["Message", "Details"], title="Nikto Error")
        return "zeuz_failed"

    # If Perl is installed and the script exists, proceed with Nikto scan
    try:
    # Construct the Nikto command and execute it
        nikto_command = ["perl", NIKTO_SCRIPT_PATH, "-h", nikto_target]
        result = subprocess.run(nikto_command, check=True)
        
        output_file_path = "/home/antu/Desktop/nikto_scan_result.txt"
        save_report_to_file(result.stdout, output_file_path)

        print(result.stdout)  # Print the output of the Nikto scan
        return "passed"
    except subprocess.CalledProcessError as e:
        print("An error occurred while running Nikto:")
        print(e.stderr)
        return "zeuz_failed"