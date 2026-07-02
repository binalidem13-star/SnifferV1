import os
import sys
import time
from scapy.all import sniff, IP, TCP, UDP, ICMP

banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⣶⣶⠶⠿⠿⠛⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠛⠿⠷⢶⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⡶⠿⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣷⠖⠲⢶⣖⢦⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠟⠛⠉⣀⠤⠤⠶⠶⠶⠶⢦⣤⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⣀⣠⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠏⠀⠀⠀⠈⢻⣧⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⠛⣩⡴⠶⠶⠚⠛⠿⠶⠶⠶⣤⣀⣀⠈⠙⠻⢿⣿⡟⢿⡷⠶⠶⠾⠿⠿⢿⣤⣤⣄⣀⡀⠀⠀⠀⠀⣼⡏⠀⠀⢀⠀⢰⣴⡏⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠋⢠⡾⠁⢀⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠈⢙⡓⠀⠀⠘⠻⣄⠙⣦⡀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⣶⣦⣼⡟⠀⠀⠀⣾⢀⣿⣿⠁⠀
⠀⠀⠀⠀⠀⠀⢀⡴⠛⣥⠀⡼⡿⠁⣰⣿⣿⡿⠓⠋⠉⢷⣦⣄⡀⠀⠀⠀⠙⠦⣈⢦⡀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣤⣶⢶⣾⣿⣿⣿⠃⠀⠀
⠀⠀⠀⠀⠀⣰⠏⠀⣴⣷⡿⢻⡇⢀⣿⠟⡡⠂⠀⠀⠀⠀⠙⠷⢿⣶⣄⡀⠀⠀⠉⢫⣷⡀⠀⠀⠀⠈⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠇⠉⠙⣾⣿⣿⠃⠀⠀⠀
⠀⠀⠀⢀⠞⠁⣠⡾⠛⠁⠀⢸⠃⣾⡯⡼⠁⠀⠀⠀⠀⠀⠀⠀⠈⣿⠹⠿⢦⣄⡀⠀⠙⢿⡀⠀⠀⠀⠀⠹⣦⡀⠀⠀⠀⠀⠀⠀⢠⠏⠀⠀⢠⣿⣿⠁⠀⠀⠀⠀
⠀⠀⠠⠋⣠⠞⠉⠀⠀⠀⠀⢸⢀⣿⣼⠁⠀⠀⠀⠀⠀⠀⠀⢀⣷⣾⠟⠉⠉⠉⠻⢦⡀⠀⠙⢦⠀⠀⠀⠀⡘⣷⡄⠀⠀⠀⠀⢀⡟⠀⠀⢀⣾⣯⠃⠀⠀⠀⠀⠀
⠀⠠⢡⠞⠁⠀⠀⠀⠀⠀⠀⢸⠘⡿⢈⠧⡀⠀⠀⠀⠀⠀⢀⣾⠟⠁⢀⣴⣶⣦⣄⠈⢻⣄⠀⠈⠳⡀⠀⠀⠈⢾⣿⣆⠀⠀⠀⡼⠁⠀⣴⣼⣿⠁⠀⠀⠀⠀⠀⠀
⢠⠝⠁⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⣿⢈⡷⠿⠦⠶⣤⣀⣴⡿⠃⠀⣰⡿⠛⢿⣿⣿⠀⣼⣿⣦⠀⠀⠀⡆⠀⠀⠀⠙⣿⣦⠀⣸⠁⠀⢰⣻⣿⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠸⡞⠀⠀⢀⣀⠀⣉⣹⣷⠴⠾⠿⠿⠶⠿⣿⡥⠞⢻⣿⢙⣧⠀⠀⣿⠀⠀⠀⢠⡘⣿⣧⠃⠀⢀⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢘⣧⣰⣿⡟⣿⣿⠟⠙⣿⣧⣄⠀⠀⠀⠀⢀⣤⣴⣟⠋⢨⣿⣇⠀⣿⡆⠀⢸⠀⣿⣿⠃⠀⢀⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠈⣿⣽⡿⠿⣿⡿⠀⠀⣿⣿⣿⣦⡤⠈⠙⠋⢀⣼⡏⠀⣿⣿⣿⡄⢹⣿⠀⢸⠃⣿⠇⠀⢀⣾⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⡄⢻⣿⣷⣄⠉⢀⠔⠈⠛⠛⠈⠉⠀⠀⣀⣴⣿⣯⡇⠀⣿⣿⣿⡇⣸⣿⠀⢸⡀⡟⠀⢀⣼⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠈⢿⣿⣯⣽⢿⣀⣀⣀⣤⡤⢴⢲⠛⣉⡴⣽⠏⠀⢀⣟⣿⡿⣳⣿⠋⠀⣿⣷⠃⢀⣾⣿⡿⣷⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⣷⡈⢿⣿⣿⣷⣿⡼⣭⡤⢧⢼⣛⣿⡿⣾⡟⠀⣴⣿⣿⠏⣸⠟⠁⠀⢸⣿⠃⠀⢈⣿⡿⣿⣿⣿⠿⠿⠿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡹⣷⡄⠻⣿⣿⣿⠛⠻⢛⣟⣿⡯⠿⣾⠏⢀⣾⣿⡿⠁⣴⡋⠀⠀⠀⣿⠇⠀⢀⣾⣿⢳⡟⠀⠹⣆⠀⠀⠈⠛⢦⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⡌⠿⣷⣌⢻⣿⣿⡌⡟⠁⢠⣄⣀⠚⣀⣼⣿⠟⢠⠟⢡⡇⠀⠀⠀⡟⠀⢀⣾⣿⢣⣿⡇⠀⠀⠘⢆⠀⠀⠀⠀⠙⣶⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⢷⣮⣙⣻⣮⣙⡿⣶⢶⣫⣷⣶⣶⣶⣿⠃⣰⡏⠀⢸⡇⠀⠀⡾⠀⠀⣼⣿⠏⠋⢿⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠈⣿⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣭⣿⣻⢿⣷⣍⠻⣿⣿⣿⡿⣿⠃⢰⣿⠁⠀⢸⣷⠀⣼⠁⢀⣼⣿⡟⠀⠀⠸⠀⠀⠀⣄⠀⠀⢸⡀⠀⠀⠀⠸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡾⠟⠉⣿⢿⣿⣿⣼⣿⣿⣦⡙⠿⣿⠇⢠⣿⡇⠀⠀⢸⣿⣳⠃⠀⢨⣿⡟⠁⠀⠀⠀⡀⠀⠀⢹⡄⠀⠀⣧⠀⠀⠀⠀⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠟⠉⠀⠀⢸⣿⠘⡇⢿⡇⣿⠈⢿⣿⡆⣿⠀⣼⣿⡇⠀⠀⣸⢳⠇⠀⢀⣿⡟⠀⠀⡆⠀⠀⢹⡄⠀⠀⢧⠀⠀⣿⣦⠀⢰⣴⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⠃⠀⡾⠀⠀⢸⡇⠀⡇⢸⡇⣿⣷⠺⢿⡷⣿⠀⣿⣿⡇⠀⠀⢳⠇⠀⢀⣿⡿⣡⠀⠀⣧⠀⠀⢸⣷⠀⠀⢸⡇⠀⢹⣿⣷⣼⡿⠿
⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⠁⡄⠀⣇⠀⠀⠈⠇⠀⣀⣸⣿⡿⠁⠀⢀⣀⣸⣶⣿⣿⣷⡀⢠⠟⠀⣠⣿⡿⢡⣿⠀⢀⣿⠀⠀⣸⣿⡄⠀⢸⣿⡄⢸⣿⡟⣿⣇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⠏⠃⢀⡇⠀⣿⠀⠀⣠⠖⠛⠟⢁⡞⠁⠀⣴⡿⣯⠙⠳⡄⠈⢭⣠⢿⣀⣾⣽⣿⢡⣿⣿⣦⣾⣿⣷⣼⣿⣿⣿⡄⣼⣿⢿⣼⣿⡇⢿⣿⡆
⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⢸⡇⣸⠿⣠⡞⠁⠀⠀⢀⡞⠀⠀⢰⡟⠃⠈⢣⡀⠀⣤⣄⣺⣿⣻⣿⣿⢣⣿⣿⣿⡟⣿⣿⣿⣿⡇⣿⣿⣿⣿⡗⢸⣿⣿⠇⠀⠻⠃
⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⢠⣿⣡⠷⠛⡟⠀⠀⣀⠀⠸⠁⠀⠀⣿⡟⠀⠀⠈⣯⣦⡵⠟⣿⣉⠘⢿⣻⣿⣿⣿⣿⠃⠹⣿⣿⡟⠁⢿⣿⣿⣿⣇⠀⢹⣿⣆⠀⣄⠀
⠀⠀⠀⠀⠀⠀⠀⢰⣿⠂⣼⢿⠇⠀⣼⠁⠀⢰⡇⠀⢸⠀⠀⣷⣿⣿⣤⣀⣴⠾⠻⣇⠀⠘⢿⣦⢜⡿⣿⣿⣿⣿⣄⠀⠙⣿⣧⡀⢠⣿⣿⣿⠏⠀⠘⠿⠏⢸⣿⠀
⠀⠀⠀⠀⠀⠀⠀⢜⡏⣰⠃⡁⠀⢠⠏⠀⠀⣾⡇⠀⢸⡆⣸⢻⣿⣿⡟⠉⠙⣦⡀⠘⢷⡀⠀⣹⡟⢹⣸⣿⣿⡏⢹⡄⢀⣿⠟⠁⠻⣿⣿⡀⠀⢰⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣾⣷⠏⢰⡇⠀⣸⠀⠀⢰⣿⣧⣤⣿⣇⣿⡈⢻⣿⣿⣆⠀⠈⠻⡆⢨⣷⡞⣹⠷⠛⢿⣿⡏⠀⠸⠃⠈⢻⣷⡀⠀⢻⣿⠁⠀⠛⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠸⣿⣿⣀⣼⣇⠀⣿⣧⣤⣿⠟⢻⣿⣿⣿⡟⠛⠸⣿⣿⣿⣷⡀⣀⣼⣏⡰⠛⠉⠀⠀⠈⠿⠇⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢉⠸⣿⣿⠿⣿⣿⠿⣿⣿⡆⠀⠟⠈⢹⣿⡀⣶⠻⡇⠹⢿⠿⣥⠾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠸⠆⠸⠟⠀⠀⠙⠀⠛⠋⠁⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

def ban():
    for line in banner.splitlines():
        print(line)
        time.sleep(0.030)

current_filter = None

def packet_callback(packet):
    global current_filter
    try:
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            proto_name = "OTHER"
            if packet.haslayer(TCP):
                proto_name = f"TCP {packet[TCP].sport} -> {packet[TCP].dport}"
            elif packet.haslayer(UDP):
                proto_name = f"UDP {packet[UDP].sport} -> {packet[UDP].dport}"
            elif packet.haslayer(ICMP):
                proto_name = "ICMP"

            # Apply filter
            if current_filter == "1" and not packet.haslayer(TCP):
                return
            elif current_filter == "2" and not packet.haslayer(UDP):
                return
            elif current_filter == "3" and not packet.haslayer(ICMP):
                return

            print(f"SRC: {src_ip:<15} | DST: {dst_ip:<15} | PROTO: {proto_name}")
    except Exception:
        pass

def start_sniffer():
    global current_filter
    os.system("cls" if os.name == "nt" else "clear")
    ban()
    print("=======================================================")
    print("               NETWORK PACKET SNIFFER")
    print("=======================================================")
    print("[1] Filter: TCP Only")
    print("[2] Filter: UDP Only")
    print("[3] Filter: ICMP Only")
    print("[4] No Filter (Show All)")
    print("[0] Back to Main Menu")
    print("=======================================================\n")
    
    choice = input("Select an option: ")
    
    if choice == "0":
        return
    elif choice in ["1", "2", "3", "4"]:
        current_filter = choice
    else:
        print("[!] Invalid choice. Returning to main menu...")
        time.sleep(2)
        return

    os.system("cls" if os.name == "nt" else "clear")
    ban()
    filter_names = {"1": "TCP Only", "2": "UDP Only", "3": "ICMP Only", "4": "All Traffic"}
    print(f"\n[+] Sniffing started (Filter: {filter_names[choice]})")
    print("[!] Press CTRL+C to stop sniffing and return to the menu.\n")
    
    try:
        if current_filter == "1":
            sniff(prn=packet_callback, store=False, filter="tcp")
        elif current_filter == "2":
            sniff(prn=packet_callback, store=False, filter="udp")
        elif current_filter == "3":
            sniff(prn=packet_callback, store=False, filter="icmp")
        else:
            sniff(prn=packet_callback, store=False)
    except KeyboardInterrupt:
        print("\n[!] Sniffing stopped.")
    except Exception as e:
        print(f"\n[!] Error: {e}")

    print("\n=======================================================")
    input("Press ENTER to return...")

if __name__ == "__main__":
    start_sniffer()