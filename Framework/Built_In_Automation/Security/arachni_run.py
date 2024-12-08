import os
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../../.."))
ARACHNI_DIR = os.path.join(BASE_DIR, "tools", "security", "arachni")
ARACHNI_EXECUTABLE = os.path.join(ARACHNI_DIR, "bin", "arachni")
ARACHNI_REPORTER_EXECUTABLE = os.path.join(ARACHNI_DIR, "bin", "arachni_reporter")

OUTPUT_FILE = "output.afr"
HTML_REPORT_FILE = "output.html"


def run_arachni_scan(target_url: str):
    """Run an Arachni scan for the target website."""
    if not os.path.exists(ARACHNI_EXECUTABLE):
        print("Arachni is not installed or the path is incorrect.")
        return
    print(f"Running Arachni scan on {target_url}...")
    subprocess.run([ARACHNI_EXECUTABLE, target_url, "--report-save-path", OUTPUT_FILE], check=True)
    print(f"Scan complete. Results saved to {OUTPUT_FILE}.")


def generate_report_from_afr():
    """Generate a report from the existing .afr file and delete the .afr file afterward."""
    if not os.path.exists(OUTPUT_FILE):
        print(f"{OUTPUT_FILE} not found.")
        return
    print(f"Generating HTML report from {OUTPUT_FILE}...")
    subprocess.run([ARACHNI_REPORTER_EXECUTABLE, OUTPUT_FILE, "--reporter=html:" + HTML_REPORT_FILE], check=True)
    print(f"HTML report saved to {HTML_REPORT_FILE}.")
    # Delete the .afr file after generating the report
    print(f"Deleting {OUTPUT_FILE}...")
    os.remove(OUTPUT_FILE)
    print(f"{OUTPUT_FILE} deleted.")
