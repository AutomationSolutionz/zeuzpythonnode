import os
import subprocess
import shutil
import sys
from urllib.parse import urlparse
from tabulate import tabulate


def extract_target(url: str) -> str:
    """
    Extracts and cleans the target from a given URL to ensure compatibility with nmap.
    """
    parsed_url = urlparse(url)
    target = parsed_url.hostname or parsed_url.netloc
    if target.startswith("www."):
        target = target[4:]
    return target


def check_perl_installed() -> bool:
    """
    Checks if Perl is installed on the system by running 'perl -v'.
    """
    try:
        # Try running 'perl -v' to check if Perl is installed
        subprocess.run(["perl", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def display_table(data: list, headers: list, title: str = "Report") -> None:
    """
    Display a formatted table in the terminal.
    """
    print(f"\n{title.center(60, '-')}\n")
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))


def save_report_to_file(output: str, file_path: str) -> None:
    """
    Args:
        output (str): The content to save to the file.
        file_path (str): The file path where the content should be saved.
    Raises:
        Exception: If the file cannot be written.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write the output to the file
        with open(file_path, "w") as file:
            file.write(output.strip())
        
        print(f"Report saved successfully to {file_path}")
    except Exception as e:
        print(f"Failed to save report to {file_path}: {e}")