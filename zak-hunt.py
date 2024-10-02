#!/usr/bin/python3
# ZAK-Hunt - Multi-threaded Port Scanner with Dirsearch integration
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
 
███████╗ █████╗ ██╗  ██╗      ██╗  ██╗██╗   ██╗███╗   ██╗████████╗
╚══███╔╝██╔══██╗██║ ██╔╝      ██║  ██║██║   ██║████╗  ██║╚══██╔══╝
  ███╔╝ ███████║█████╔╝ █████╗███████║██║   ██║██╔██╗ ██║   ██║   
 ███╔╝  ██╔══██║██╔═██╗ ╚════╝██╔══██║██║   ██║██║╚██╗██║   ██║   
███████╗██║  ██║██║  ██╗      ██║  ██║╚██████╔╝██║ ╚████║   ██║   
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝      ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
                                                                  
   zak-hunt v1.1
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

    # Automatically run the full Nmap scan
    print("-" * 60)
    print("Running full Nmap scan...")
    try:
        full_nmap_cmd = "nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target)
        print(full_nmap_cmd)  # Show the Nmap command that will be executed
        os.mkdir(target)  # Create a directory for saving results
        os.chdir(target)  # Change to the new directory
        os.system(full_nmap_cmd)  # Execute the full Nmap scan
        t3 = datetime.now()
        total1 = t3 - t1
        print("-" * 60)
        print("Full Nmap scan completed in " + str(total1))
        print("Press enter to quit...")
        input()
    except FileExistsError as e:
        print(e)
        exit()

    def dirsearch_scan():
        print("-" * 60)
        print("Would you like to perform a Dirsearch scan?")
        print("1 = Yes, for Directory Busting")
        print("2 = No, Skip Dirsearch")
        choice = input("Option Selection: ")

        if choice == "1":
            wordlist = input("Enter the path to your wordlist for directories: ")
            dirsearch_cmd = f"dirsearch -u http://{target} -w {wordlist}"
            print("Running Dirsearch...")
            try:
                result = subprocess.run(dirsearch_cmd, shell=True, capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"Error running Dirsearch: {e}")
        else:
            return

    dirsearch_scan()

if __name__ == '__main__':
    target = input("Enter your target IP address or URL here: ")
    zak_hunt(target)
