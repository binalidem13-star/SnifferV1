import numpy as np
import os 
import time
import sys
import ctypes
import wifi_info
import wifi_sniffer
import signal_sniffer
import dns_sniffer
import web_scanner
import port_scanner

if sys.platform == "win32":
    os.system("title SnifferV1")
else:
    sys.stdout.write("\x1b]2;SnifferV1\x07")
    sys.stdout.flush()


def show_info():
    text = """
************************************************************
                SNIFFERV1 - INFO & COMMUNITY            
************************************************************
 Developer:   Dxrk 
 Version:     1.0.0 
------------------------------------------------------------
 I would be delighted if you joined our Discord server. 
 You can find extensive resources and tutorials on 
 cybersecurity in the channels at the bottom of the server.

 Discord Link: https://discord.com/invite/uGw6j6AKgc
------------------------------------------------------------
 SUPPORT THE PROJECT:
 If this tool is useful to you, please consider giving
 the repository a Star on GitHub. It motivates me to
 keep improving this project and developing new ones.

 GitHub Link:  https://github.com/binalidem13-star
************************************************************
"""
    print(text)
    input("Press ENTER to return to the main menu...")


def admin_inquiry():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            " ".join(sys.argv),
            None,
            1
        )
        sys.exit(0)
admin_inquiry()


try:
    import winreg
    
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "DisableLocation")
        winreg.CloseKey(key)
    except Exception:
        pass

    key2 = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location")
    winreg.SetValueEx(key2, "Value", 0, winreg.REG_SZ, "Allow")
    winreg.CloseKey(key2)
except Exception:
    pass

banner = """
                            ███████╗███╗   ██╗██╗███████╗███████╗███████╗██████╗ ██╗   ██╗ ██╗
                            ██╔════╝████╗  ██║██║██╔════╝██╔════╝██╔════╝██╔══██╗██║   ██║███║
                            ███████╗██╔██╗ ██║██║█████╗  █████╗  █████╗  ██████╔╝██║   ██║╚██║
                            ╚════██║██║╚██╗██║██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██╗╚██╗ ██╔╝ ██║
                            ███████║██║ ╚████║██║██║     ██║     ███████║██║  ██║ ╚████╔╝  ██║
                            ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝  ╚═══╝   ╚═╝
                                                            by dxrk                                                       
"""

def options():  
    
    print("Type I for Info")
    print("[1] WIFI Info ")
    print("[2] WIFI Sniffer")       
    print("[3] Signal Sniffer")
    print("[4] DNS Sniffer")
    print("[5] Full Web scanner & Info")
    print("[6] show wifi ports")

os.system("cls")


while True:
    print(banner)
    options()



    tar = input("\n>")

    if tar == "1":
        wifi_info.show_details()
        input("\n press enter to go back..")
        os.system("cls")

    elif tar == "2":
        wifi_sniffer.start_sniffer()
        os.system("cls")

    elif tar == "3":
        signal_sniffer.start_signal_sniffer()
        os.system("cls")

    elif tar == "4":
        dns_sniffer.start_dns_sniffer()
        os.system("cls")

    elif tar == "5":
        web_scanner.start_web_scanner()
        os.system("cls")

    elif tar == "6":
        port_scanner.start_port_scanner()
        os.system("cls")

    elif tar == "I":
        show_info()
        os.system("cls")

    elif tar == "i":
        show_info()
        os.system("cls")

    else:
        print("\n[!] Invalid input")
        time.sleep(2)
        os.system("cls")



                        
