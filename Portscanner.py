# Seth Martin
# CYBR-260-40A
# Final Project
# 02/28/2020
#
# Description:
#   Port scanner for educational purposes / home use. Will take an IP provided from the user and gives them 2 choices
#   between top 20 TCP ports and top 1000 TCP ports which is much slower as there is no threading at the moment.
#   RECOMMENDED: Use top 20 TCP ports for now
#
# TODO: Add threading to make top 1000 TCP ports faster.


import socket
import subprocess
from portlist import ports_1000, ports_20
import sys
import datetime
import os

# create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# getting Host IP address. Will probably make this an argument later.
server_ip = input("Enter server IP : ")

# grabbing IP of a network name such as a NAS device i.e. name: diskstation
remoteServerIP = socket.gethostbyname(server_ip)

# assigning the time now to tn
tn = datetime.datetime.now()


# using subprocess to call ping command with server_ip
def ping():
    # nice little ping banner
    print("=" * 60)
    print(" " * 10, f"Pinging the target IP {server_ip}")
    print("=" * 60)

    # calling ping command via subproccess, stdout to hide output of ping
    p = subprocess.call(f"ping {server_ip}", stdout=subprocess.PIPE, shell=True)
    if p == 0:  # returns is up if true, else it's down
        print(f"\n[+] {server_ip} is up\n")
    else:
        print(f"[-] {server_ip} is down\n")
        print("Try using a different IP address.")
        exit()


# scanning top 1000 TCP ports reference list contained in portlist.py file
def scan_1000():
    # banner
    print("=" * 60)
    print(" " * 10, f"Starting port scan of {server_ip}")
    print(" " * 10, f"Time now: {tn}")
    print("=" * 60)

    i = 0
    # checking if file already exists
    while os.path.exists(f"results{i}.csv"):
        i += 1
    # if results0.csv doesn't exist this is the first filename, then increment
    with open(f"results{i}.csv", "a") as f:
        try:
            for port in ports_1000:  # iterating over ports from portlist file
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((remoteServerIP, port))  # try connecting to ports
                if result == 0:  # should return true if open
                    value = f", {remoteServerIP},{port},OPEN\n"
                    v = str(value)
                    f.write(v)
                    try:
                        service = socket.getservbyport(port)
                    except Exception:
                        service = "unknown"
                    print(f"[+] PORT: {port}\tSERVICE: {service}\t Open")
                sock.close()
            print(f"\nScan complete, exporting results to results{i}.csv")
        # in case user wants to terminate the program
        except KeyboardInterrupt:
            print("User pressed Ctrl-C. Exiting")
            exit()

        # This exception is raised for address-related errors, for getaddrinfo() and getnameinfo().
        except socket.gaierror:
            print('Hostname could not be resolved. Exiting')
            exit()
    f.close()  # closing file


# scanning for the top 20 TCP ports reference list contained in portlist.py
def scan_20():
    # banner
    print("=" * 60)
    print(" " * 10, f"Starting port scan of {server_ip}")
    print(" " * 10, f"Time now: {tn}")
    print("=" * 60)

    i = 0
    while os.path.exists(f"results{i}.csv"):
        i += 1
    with open(f"results{i}.csv", "a") as f:
        try:
            for port in ports_20:  # iterating over ports from portlist file
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((remoteServerIP, port))  # try connecting to ports
                if result == 0:  # should return true if open
                    value = f",{remoteServerIP},{port},OPEN\n"
                    v = str(value)
                    f.write(v)
                    try:
                        service = socket.getservbyport(port)
                    except Exception:
                        service = "unknown"
                    print(f"[+] PORT: {port}\tSERVICE: {service}\t Open")
                sock.close()
            print(f"Scan complete, exporting to results{i}.csv")
        # in case user wants to terminate the program
        except KeyboardInterrupt:
            print("User pressed Ctrl-C, exiting now.")
            exit()

        # this exception is raised for address-related errors, for getaddrinfo() and getnameinfo().
        except socket.gaierror:
            print('Hostname could not be resolved. Exiting')
            exit()
    f.close()  # closing file


# making sure the user selects either 1 or 2 to proceed
# if 1 or 2 is selected the corresponding scan function will initiate.
# probably a better way of doing this but short on time
def main():
    print("1) Top 1000 TCP ports (SLOW: This CAN take up to 10-15 minutes)\n2) Top 20 TCP ports (FASTER)")
    scanType = input()
    if scanType == "1":
        print("\n[+] Stating scan for top 1000 TCP ports\n")
        ping()
        scan_1000()
        exit()
    elif scanType == "2":
        print("\n[+] Starting scan for top 20 TCP ports\n")
        ping()
        scan_20()
        exit()

    while scanType != "1" or scanType != "2":
        print("1) Top 1000 TCP ports\n2) Top 20 TCP ports")
        scanType = input()
        if scanType == "1":
            print("\n[+] Stating scan for top 1000 TCP ports\n")
            ping()
            scan_1000()
            exit()
        elif scanType == "2":
            print("\n[+] Starting scan for top 20 TCP ports\n")
            ping()
            scan_20()
            exit()


main()
