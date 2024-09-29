# ZAK-Hunt

**ZAK-Hunt** is a multi-threaded port scanner and directory busting tool designed for penetration testing and network reconnaissance. It includes port scanning capabilities with integration for [Nmap](https://nmap.org/) and [Gobuster](https://github.com/OJ/gobuster), making it a versatile tool for exploring vulnerabilities and analyzing network services.

## Features

- Multi-threaded port scanning across all 65,535 ports.
- Suggests detailed **Nmap** commands for further exploration of open ports.
- Integrated **Gobuster** for directory and DNS subdomain busting.
- Displays scan duration for efficient time tracking.
- Supports web, mobile, and PC IP addresses.
- Compatible with both IPv4 and domain names.

## Requirements

- Python 3.x
- [Nmap](https://nmap.org/download.html) (ensure Nmap is installed on your system and added to your path)
- [Gobuster](https://github.com/OJ/gobuster) (ensure Gobuster is installed)

## Installation
   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-repo/zak-hunt.git
```

### Change permissions for the file zak-hunt.py:

```1.bash
sudo chmod +x zak-hunt.py
```
```2.bash
sudo ln -s $(pwd)/zak-hunt.py /usr/local/bin/zak-hunt
```

## Usage
To run ZAK-Hunt, open a terminal and navigate to the directory where the script is located. Then run the following command:

```bash
python3 zak-hunt.py
```
## Example usage:
Enter the target's IP address or domain name when prompted:

```bash
Enter your target IP address or URL here: 192.168.1.1
```
The tool will start scanning ports, displaying which ones are open. After the scan is complete, it will recommend an Nmap scan for further analysis.

You will also be prompted to run Gobuster for directory or DNS subdomain busting:

Option 1: Directory busting
Option 2: DNS subdomain busting
Option 3: Skip Gobuster
After the scan is completed, you can choose to:

Run the recommended Nmap scan.
Run another ZAK-Hunt scan on a different target.
Exit the tool.

## Example Output
```bash

 
███████╗ █████╗ ██╗  ██╗      ██╗  ██╗██╗   ██╗███╗   ██╗████████╗
╚══███╔╝██╔══██╗██║ ██╔╝      ██║  ██║██║   ██║████╗  ██║╚══██╔══╝
  ███╔╝ ███████║█████╔╝ █████╗███████║██║   ██║██╔██╗ ██║   ██║   
 ███╔╝  ██╔══██║██╔═██╗ ╚════╝██╔══██║██║   ██║██║╚██╗██║   ██║   
███████╗██║  ██║██║  ██╗      ██║  ██║╚██████╔╝██║ ╚████║   ██║   
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝      ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
                                                                  
   zak-hunt v1.0


------------------------------------------------------------
Scanning target 192.168.1.1
Time started: 2024-09-29 14:00:00
------------------------------------------------------------
Port 22 is open
Port 80 is open
...
Port scan completed in 0:01:35
------------------------------------------------------------
ZAK-Hunt recommends the following Nmap scan:
************************************************************
nmap -p22,80 -sV -sC -T4 -Pn -oA 192.168.1.1 192.168.1.1
************************************************************
Would you like to run Nmap or quit to terminal?
------------------------------------------------------------
1 = Run suggested Nmap scan
2 = Run another ZAK-Hunt scan
3 = Exit to terminal
Option Selection:

```
## License


ZAK-Hunt is licensed under the GNU GPLv3.

