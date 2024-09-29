#!/usr/bin/python3
# ZAK-Hunt - Multi-threaded Port Scanner with Gobuster integration
# Author: Moataz Zaky
# v1.1
# https://eli0zak.github.io/
# Licensed under GNU GPLv3 Standards.  https://www.gnu.org/licenses/gpl-3.0.en.html

import socket
import os
import threading
import sys
from queue import Queue
from datetime import datetime
import subprocess
logo = """
  ______     _    _             _   
 |__  (_)   | |  | |           | |  
    ) | _ __| | _| |_   _  __ _| |_ 
   / / | '__| |/ / | | | |/ _` | __|
  / /_ | |  |   <| | |_| | (_| | |_ 
 /____|_|  |_|\_\_|\__,_|\__,_|\__|
 
   fsociety v1.0
"""

author_info = "Author: mo3tazaky@hotmail.com"

def zak_hunt(target):
    socket.setdefaulttimeout(0.30)
    print_lock = threading.Lock()
    discovered_ports = []

    print("-" * 60)
    print(logo)
    print(author_info)
    print("-" * 60)

    try:
        t_ip = socket.gethostbyname(target)
    except (UnboundLocalError, socket.gaierror):
        print("\n[-] Invalid format. Please use a correct IP or web address [-]\n")
        sys.exit()

    print("-" * 60)
    print("Scanning target " + t_ip)
    print("Time started: " + str(datetime.now()))
    print("-" * 60)
    t1 = datetime.now()

    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            portx = s.connect((t_ip, port))
            with print_lock:
                print("Port {} is open".format(port))
                discovered_ports.append(str(port))
            portx.close()
        except (ConnectionRefusedError, AttributeError, OSError):
            pass

    def threader():
        while True:
            worker = q.get()
            portscan(worker)
            q.task_done()

    q = Queue()

    for x in range(200):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for worker in range(1, 65536):
        q.put(worker)

    q.join()

    t2 = datetime.now()
    total = t2 - t1
    print("Port scan completed in " + str(total))
    print("-" * 60)
    print("ZAK-Hunt recommends the following Nmap scan:")
    print("*" * 60)
    print("nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target))
    print("*" * 60)
    nmap = "nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target)

    def gobuster_scan():
        print("-" * 60)
        print("Would you like to perform a Gobuster scan?")
        print("1 = Yes, for Directory Busting")
        print("2 = Yes, for DNS Subdomain Busting")
        print("3 = No, Skip Gobuster")
        choice = input("Option Selection: ")

        if choice == "1":
            wordlist = input("Enter the path to your wordlist for directories: ")
            gobuster_cmd = f"gobuster dir -u http://{target} -w {wordlist}"
        elif choice == "2":
            wordlist = input("Enter the path to your wordlist for DNS: ")
            gobuster_cmd = f"gobuster dns -d {target} -w {wordlist}"
        else:
            return

        print("Running Gobuster...")
        try:
            result = subprocess.run(gobuster_cmd, shell=True, capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"Error running Gobuster: {e}")

    gobuster_scan()

    def automate():
        choice = '0'
        while choice == '0':
            print("Would you like to run Nmap or quit to terminal?")
            print("-" * 60)
            print("1 = Run suggested Nmap scan")
            print("2 = Run another ZAK-Hunt scan")
            print("3 = Exit to terminal")
            print("-" * 60)
            choice = input("Option Selection: ")
            if choice == "1":
                try:
                    print(nmap)
                    os.mkdir(target)
                    os.chdir(target)
                    os.system(nmap)
                    t3 = datetime.now()
                    total1 = t3 - t1
                    print("-" * 60)
                    print("Combined scan completed in " + str(total1))
                    print("Press enter to quit...")
                    input()
                except FileExistsError as e:
                    print(e)
                    exit()
            elif choice == "2":
                zak_hunt(target)
            elif choice == "3":
                sys.exit()
            else:
                print("Please make a valid selection")
                automate()

    automate()

if __name__ == '__main__':
    target = input("Enter your target IP address or URL here: ")
    zak_hunt(target)
