import os
import sys
import subprocess
import time
import re

Banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡶⠲⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣤⠝⠛⠿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠉⠀⠀⠀⠀⠀⠈⢿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡟⡵⣠⣊⣤⠶⠒⠀⠘⢦⣄⣹⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⢏⣼⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠟⠚⠁⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣶⣝⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⣠⠆⠀⠀⢀⣴⣾⡋⠿⠃⣿⠘⠹⠻⣿⣿⣧⢹⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⠀⣰⠃⠀⢀⣴⣿⢿⣾⡇⠀⢸⣿⡄⠀⣀⣿⣿⣿⢀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣇⠀⡀⢠⡏⠀⢠⣿⠁⢿⣼⣿⣿⣤⡿⢻⣤⣾⣿⣿⣿⡿⣸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣆⢳⣸⣇⢀⣿⣿⣇⠀⣙⡛⠛⣿⣵⣿⣛⠋⢀⣿⣿⢳⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣈⣻⣯⣻⣿⠘⣿⡇⢹⣿⣿⡇⠀⠁⠉⠁⢸⣷⣾⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠾⣛⠋⢛⠛⠻⣷⣝⠧⢻⣿⣌⠁⢿⣧⣾⣾⣿⣷⣼⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⢻⣿⠻⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣰⣿⢁⣴⣿⣄⣸⡇⠰⢮⣿⣆⠈⢻⣿⣆⢸⣇⣈⣉⣀⣰⣿⣿⣿⠿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁⣴⡟⢻⣇⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣴⠾⠋⠿⡿⠛⠛⠉⠙⢿⡇⢠⡄⠹⣿⣧⡀⠙⠿⠖⠚⣻⣿⣿⣿⣟⡋⢉⣴⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⢧⣾⠿⣧⠙⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣾⣏⡅⠀⠀⠀⣤⣀⡀⠀⠀⠀⢸⣼⣧⡀⠈⢻⣷⣄⣠⣴⣾⣿⡿⢹⠉⠙⠛⠛⠛⠛⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⡅⠀⠈⢷⡈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢻⣿⠋⠀⠀⠀⠀⠀⠈⠉⠙⣳⢶⣦⣿⡇⣿⡀⠀⠻⡏⠉⣰⢏⡾⠁⠀⣀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⢠⣾⡿⣫⡿⠁⠈⢷⣄⠀⠀⠁⠈⢻⡄⠀⠀⠀⠀⠀⠀⠀
⢀⣿⠁⢀⡴⢁⣠⣤⣤⣤⣤⣄⣉⠻⢿⣿⣧⢸⣧⠀⠀⠉⠀⠏⡼⠁⣠⣾⢃⣠⡴⠃⠀⠀⣿⣧⠀⠀⠀⠀⠀⢀⡴⠋⣠⡾⠋⠀⠀⠀⠈⠻⣄⠀⡄⠀⠀⢻⣄⠀⠀⠀⠀⠀⠀
⣸⡇⣠⠏⠀⢋⣥⣿⡿⠛⠋⠀⠀⣤⣌⣻⣿⣿⣿⣰⡟⠀⠀⠀⠀⠸⣻⣿⣿⠏⠀⠀⠀⠀⡿⢹⡆⠀⠀⢀⣴⢟⣷⣾⠟⠁⠀⠀⠀⠀⠀⠀⠙⢿⣷⡿⠋⠀⢻⡄⠀⠀⠀⠀⠀
⢻⣷⡟⠀⠴⢻⡿⠋⠀⢠⡶⠶⠀⠀⣉⣻⣿⣿⣿⣟⠁⠀⠀⠀⠀⠀⣿⡿⠁⠀⠀⠀⠀⠀⠳⠀⣻⡴⣾⢟⣵⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡅⠀⠀⠈⢿⡆⠀⠀⠀⠀
⠀⣿⠀⠀⢀⣿⠃⠀⢠⡿⠁⠀⠒⢋⣽⣿⠿⠟⠛⠉⠉⠉⣉⠉⠛⠛⢻⣿⣆⢀⣀⣤⡶⣿⣷⠾⢫⣄⣘⣿⡿⢋⣠⣶⣶⣶⣶⣿⡟⣻⡇⠀⠀⠀⠈⢿⣄⣠⣞⠈⢻⡄⠀⠀⠀
⢰⡏⠀⠀⢸⡇⠀⢀⡾⠀⠀⠀⢠⣾⠋⠀⠀⢀⣶⣤⠾⠛⠁⠀⣠⣼⣿⣿⣿⣿⡿⠟⣛⣿⣯⣝⣛⣾⣿⣿⣿⠟⣽⡿⢷⣽⣿⣿⣯⣽⡇⠀⠀⠀⠀⠈⠛⣿⠇⠀⠈⣷⠀⠀⠀
⢸⡇⠀⢀⢸⠃⠀⠘⠀⠀⠀⣰⡿⠃⠀⠀⢠⣿⠋⠁⠀⢀⣴⣿⠿⠿⠛⣋⣭⡾⠟⢻⣿⣿⣿⣶⣿⣿⣿⣿⡏⠀⢻⣧⣼⣻⣿⡿⣦⣿⠃⠀⠀⠀⠀⠀⠀⢿⡄⠀⠀⠹⣇⠀⠀
⢸⣇⠀⣾⡈⠀⠀⠀⠀⠀⢰⡟⠀⠀⢀⠀⣿⠃⠀⠀⣰⡿⢋⣁⣤⠶⠛⠉⠁⠀⣠⡿⣿⣿⣿⣿⣿⠉⣿⣿⢷⠀⢸⣿⣿⣿⣯⠿⠿⠇⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⣿⡀⠀
⠀⠙⠿⣿⣇⠀⠀⠀⠀⢠⠏⠀⠀⠀⢸⣰⡟⠀⠀⢸⣿⣿⣿⣿⡏⠀⠀⠀⣠⢞⣥⣴⣿⠁⠙⠻⣿⣦⠸⢿⣾⡇⠀⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡄⠀⢸⣧⠀
⠀⠀⠀⠘⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡇⠀⠀⢸⡟⠛⡿⣿⠀⠀⢠⢞⣵⡿⠛⠁⢿⣇⠀⠀⠈⠻⣷⡌⠳⢻⠀⢿⡛⠛⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⠀⠀⣿⠀
⠀⠀⠀⠀⠈⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⣄⡀⢸⣿⣿⡇⣿⢀⣴⣵⡿⠋⠀⠀⠀⠸⣿⡄⠀⠀⠀⠈⢿⣆⠀⠁⢸⣧⣾⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣇⠀⣿⡇
⠀⠀⠀⠀⠀⠈⠛⢷⣤⡀⠀⠀⠀⠛⠲⣤⡀⠀⠀⠀⢿⣿⠁⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⢻⢿⣆⠀⠀⠀⠀⠹⣆⠀⠀⢻⣯⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⢹⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠷⠶⠤⣤⣄⣹⣦⠀⠀⠘⣿⠀⣾⡟⢁⢀⣄⠀⠀⠀⠀⠀⠈⢧⡻⣦⡀⠀⠀⠀⠹⣧⣳⣤⣽⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⢸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣟⢻⣧⡀⠀⢻⠀⣿⠀⠸⣆⣿⣦⡀⠀⠀⠀⠀⠀⠁⠈⠻⣦⡀⠀⠀⠙⠻⠟⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⢛⣽⣧⡀⠀⣼⠏⠀⠀⠈⠻⣯⠻⣦⡀⠀⣀⠀⠀⠀⠀⠈⠙⢶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⣁⣴⠟⠛⢿⣷⡞⠃⢀⣀⡀⠀⠀⡉⠃⠈⠙⠂⠈⠙⠲⢤⣀⡀⠀⠀⠈⠙⠳⢶⣤⣤⣀⣀⣀⣤⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⢋⣡⠾⠋⠀⠀⠀⠀⠉⠻⢶⣤⣉⣻⢷⣶⣿⣦⣄⡀⠀⠀⠀⠀⠀⠈⠙⠳⢶⣶⠶⠶⠶⠶⠾⠟⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠁
⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⢋⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠻⢿⣿⣛⠿⠝⠓⠲⠶⢤⣤⣤⣤⣀⣀⣉⣛⣶⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⡾⢫⡴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣾⣋⡶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣠⡾⢋⡽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⠿⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

def animations():
    for _ in range(5):
        for pos in ["|", "/", "-", "\\"]:
            sys.stdout.write(pos)
            sys.stdout.flush()
            time.sleep(0.2)
            sys.stdout.write("\b")

def ban():
    for line in Banner.splitlines():
        print(line)
        time.sleep(0.030)

def get_surrounding_wifis():
    try:
        cmd = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True, errors='ignore')
        output = cmd.stdout
        if "location permission" in output.lower() or "access is denied" in output.lower():
            print("\n[!] Windows is blocking the scan. Please activate Location services in settings.")
            return []
        wifis = re.findall(r"SSID \d+ : (.+)", output)
        cl_wifi = [name.strip() for name in wifis if name.strip()]
        return cl_wifi
    except Exception:
        return []

def get_adapter_info():
    try:
        cmd = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, errors='ignore')
        output = cmd.stdout
        manufacturer = re.search(r"Hersteller|Manufacturer.*?:\s*(.+)", output)
        model = re.search(r"Beschreibung|Description.*?:\s*(.+)", output)
        driver = re.search(r"Treiber|Driver.*?:\s*(.+)", output)
        supported_standards = re.search(r"Funktyp|Radio type.*?:\s*(.+)", output)
        mcs_index = re.search(r"MCS-Index|MCS Index.*?:\s*(\d+)", output)
        channel_width = re.search(r"Kanalbreite|Channel width.*?:\s*(\d+\s*MHz)", output)
        return {
            "manufacturer": manufacturer.group(1).strip() if manufacturer else "Not found",
            "model": model.group(1).strip() if model else "Not found",
            "driver": driver.group(1).strip() if driver else "Not found",
            "supported_standards": supported_standards.group(1).strip() if supported_standards else "Not found",
            "mcs_index": mcs_index.group(1) if mcs_index else "Not found",
            "channel_width": channel_width.group(1) if channel_width else "Not found"
        }
    except Exception:
        return {
            "manufacturer": "Not found",
            "model": "Not found",
            "driver": "Not found",
            "supported_standards": "Not found",
            "mcs_index": "Not found",
            "channel_width": "Not found"
        }

def get_connection_stats():
    try:
        cmd = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, errors='ignore')
        output = cmd.stdout
        rx_rate = re.search(r"(?:Empfangsrate|Receive rate).*?:\s*([0-9.]+)", output)
        tx_rate = re.search(r"(?:Sendeleistung|Transmit power|Transmission rate).*?:\s*([0-9.]+)", output)
        signal_strength = re.search(r"Signal.*?:\s*([0-9%]+)", output)
        rssi = re.search(r"RSSI.*?:\s*(-?\d+\s*dBm)", output)
        snr = re.search(r"SNR.*?:\s*(\d+\s*dB)", output)
        return {
            "rx_rate": rx_rate.group(1) if rx_rate else "Not found",
            "tx_rate": tx_rate.group(1) if tx_rate else "Not found",
            "signal_strength": signal_strength.group(1) if signal_strength else "Not found",
            "rssi": rssi.group(1) if rssi else "Not found",
            "snr": snr.group(1) if snr else "Not found"
        }
    except Exception:
        return {
            "rx_rate": "Not found",
            "tx_rate": "Not found",
            "signal_strength": "Not found",
            "rssi": "Not found",
            "snr": "Not found"
        }

def get_ip_config():
    try:
        cmd = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True, errors='ignore')
        output = cmd.stdout
        ipv4 = re.search(r"IPv4-(?:Adresse|Address)[\.\s]*:\s*([0-9.]+)", output)
        subnet = re.search(r"(?:Subnetzmaske|Subnet Mask)[\.\s]*:\s*([0-9.]+)", output)
        gateway = re.search(r"(?:Standardgateway|Default Gateway)[\.\s]*:\s*([0-9.]+)", output)
        dhcp_server = re.search(r"(?:DHCP-Server|DHCP Server)[\.\s]*:\s*([0-9.]+)", output)
        dns_servers = re.findall(r"(?:DNS-Server|DNS Servers)[\.\s]*:\s*([0-9.]+)", output)
        lease_obtained = re.search(r"(?:Lease erhalten|Lease Obtained).*?:\s*(.+)", output)
        lease_expires = re.search(r"(?:Lease läuft ab|Lease Expires).*?:\s*(.+)", output)
        return {
            "ipv4": ipv4.group(1) if ipv4 else "Not assigned",
            "subnet": subnet.group(1) if subnet else "Not found",
            "gateway": gateway.group(1) if gateway else "Not found",
            "dhcp_server": dhcp_server.group(1) if dhcp_server else "Not found",
            "dns_servers": ", ".join(dns_servers) if dns_servers else "Not found",
            "lease_obtained": lease_obtained.group(1).strip() if lease_obtained else "Not found",
            "lease_expires": lease_expires.group(1).strip() if lease_expires else "Not found"
        }
    except Exception:
        return {
            "ipv4": "Not assigned",
            "subnet": "Not found",
            "gateway": "Not found",
            "dhcp_server": "Not found",
            "dns_servers": "Not found",
            "lease_obtained": "Not found",
            "lease_expires": "Not found"
        }

def get_neighbor_networks():
    try:
        cmd = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], capture_output=True, text=True, errors='ignore')
        output = cmd.stdout
        networks = re.findall(r"SSID \d+ : (.+?)\r?\n(?:.*?BSSID \d+ : ([0-9a-fA-F:]+).*?Signal : ([0-9%]+).*?Kanal : (\d+).*?Funktyp : (.+?)\r?\n)", output, re.DOTALL)
        return [
            {
                "ssid": net[0].strip(),
                "bssid": net[1].strip(),
                "signal": net[2].strip(),
                "channel": net[3].strip(),
                "radio_type": net[4].strip()
            }
            for net in networks
        ]
    except Exception:
        return []

def show_details():
    os.system("cls")
    ban()
    print("Searching for Wi-Fi networks... ", end="")
    animations()
    print("\n")
    wifi_list = get_surrounding_wifis()
    if not wifi_list:
        print("[!] No networks found or scan blocked by Windows.")
        return
    print("=== FOUND NETWORKS ===")
    for index, wlan_name in enumerate(wifi_list, start=1):
        print(f"[{index}] {wlan_name}")
    print("-" * 40)
    print("[0] Back to the main menu")
    try:
        choice = int(input("\nSelect a Wi-Fi for Full Info: "))
    except ValueError:
        print("[!] Please enter a valid number.")
        return
    if choice == 0:
        return
    if 1 <= choice <= len(wifi_list):
        selected_wifi = wifi_list[choice - 1]
        os.system("cls")
        print("=======================================================")
        print(f"            INFO REPORT: {selected_wifi}")
        print("=======================================================")
        cmd_deep = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], capture_output=True, text=True, errors='ignore')
        deep_output = cmd_deep.stdout
        try:
            start_pos = deep_output.lower().find(selected_wifi.lower())
            relevant_text = deep_output[start_pos:start_pos+2000]
        except Exception:
            relevant_text = deep_output
        bssid = re.search(r"BSSID \d+\s*:\s*([0-9a-fA-F:]+)", relevant_text)
        signal = re.search(r"Signal\s*:\s*([0-9%]+)", relevant_text)
        channel = re.search(r"(?:Kanal|Channel)\s*:\s*([0-9]+)", relevant_text)
        net_type = re.search(r"(?:Netzwerktyp|Network type)\s*:\s*(.+)", relevant_text)
        radio_type = re.search(r"(?:Funktyp|Radio type)\s*:\s*(.+)", relevant_text)
        auth = re.search(r"(?:Authentifizierung|Authentication)\s*:\s*(.+)", relevant_text)
        cipher = re.search(r"(?:Verschlüsselung|Encryption|Chiffre|Cipher)\s*:\s*(.+)", relevant_text)
        band = re.search(r"(?:Frequenzband|Band)\s*:\s*(.+)", relevant_text)
        channel_width = re.search(r"(?:Kanalbreite|Channel width)\s*:\s*([0-9]+\s*MHz)", relevant_text)
        print("\n[+] WIRELESS & HARDWARE DETAILS")
        print(f"    |- SSID (Name):           {selected_wifi}")
        print(f"    |- BSSID (MAC):           {bssid.group(1) if bssid else 'Not found'}")
        print(f"    |- Signal Strength:       {signal.group(1) if signal else 'Not found'}")
        print(f"    |- RSSI:                  {re.search(r'RSSI.*?:\s*(-?\d+\s*dBm)', relevant_text).group(1) if re.search(r'RSSI.*?:\s*(-?\d+\s*dBm)', relevant_text) else 'Not found'}")
        print(f"    |- Channel:               {channel.group(1) if channel else 'Not found'}")
        print(f"    |- Frequency Band:       {band.group(1).strip() if band else 'Not found'}")
        print(f"    |- Channel Width:        {channel_width.group(1) if channel_width else 'Not found'}")
        print(f"    |- Wi-Fi Standard:        {radio_type.group(1).strip() if radio_type else 'Not found'}")
        print(f"    |- Network Type:          {net_type.group(1).strip() if net_type else 'Not found'}")
        print("\n[+] SECURITY & ENCRYPTION")
        print(f"    |- Authentication:        {auth.group(1).strip() if auth else 'Not found'}")
        print(f"    |- Cipher Type:           {cipher.group(1).strip() if cipher else 'Not found'}")
        print(f"    |- WPA3 Support:          {re.search(r'WPA3', relevant_text).group(0) if re.search(r'WPA3', relevant_text) else 'No'}")
        print(f"    |- PMF (Protected Mgmt):  {re.search(r'PMF.*?(Yes|No|Aktiviert|Deaktiviert)', relevant_text).group(1) if re.search(r'PMF.*?(Yes|No|Aktiviert|Deaktiviert)', relevant_text) else 'Not found'}")
        status_cmd = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, errors='ignore')
        if selected_wifi.lower() in status_cmd.stdout.lower():
            adapter_info = get_adapter_info()
            connection_stats = get_connection_stats()
            ip_config = get_ip_config()
            print("\n[+] ADAPTER DETAILS")
            print(f"    |- Manufacturer:          {adapter_info['manufacturer']}")
            print(f"    |- Model:                 {adapter_info['model']}")
            print(f"    |- Driver:                {adapter_info['driver']}")
            print(f"    |- Supported Standards:   {adapter_info['supported_standards']}")
            print(f"    |- MCS Index:             {adapter_info['mcs_index']}")
            print(f"    |- Channel Width:         {adapter_info['channel_width']}")
            print("\n[+] ACTIVE CONNECTION PERFORMANCE")
            print(f"    |- Max Download Speed:    {connection_stats['rx_rate']} Mbps")
            print(f"    |- Max Upload Speed:      {connection_stats['tx_rate']} Mbps")
            print(f"    |- Signal Strength:      {connection_stats['signal_strength']}")
            print(f"    |- RSSI:                  {connection_stats['rssi']}")
            print(f"    |- SNR:                   {connection_stats['snr']}")
            print("\n[+] IP & NETWORK CONFIGURATION (CONNECTED)")
            print(f"    |- Local IPv4:            {ip_config['ipv4']}")
            print(f"    |- Subnet Mask:           {ip_config['subnet']}")
            print(f"    |- Router IP (GW):        {ip_config['gateway']}")
            print(f"    |- DHCP Server:           {ip_config['dhcp_server']}")
            print(f"    |- DNS Server(s):         {ip_config['dns_servers']}")
            print(f"    |- Lease Obtained:        {ip_config['lease_obtained']}")
            print(f"    |- Lease Expires:         {ip_config['lease_expires']}")
        else:
            print("\n[-] PC NETWORK INFOS")
            print("    [!] You are not connected to this network.")
            print("        Connect to this Wi-Fi to unlock live IP & speed reports.")
        neighbor_networks = get_neighbor_networks()
        if neighbor_networks:
            print("\n[+] NEARBY NETWORKS (Channel Utilization)")
            for net in neighbor_networks[:5]:
                print(f"    |- SSID: {net['ssid']}, BSSID: {net['bssid']}, Channel: {net['channel']}, Signal: {net['signal']}, Radio: {net['radio_type']}")
        print("\n=======================================================")
        input(" Press ENTER to return to the main menu...")
    else:
        print("[!] Invalid Number.")

if __name__ == "__main__":
    while True:
        try:
            show_details()
        except KeyboardInterrupt:
            print("\n[!] Exiting...")
            break
