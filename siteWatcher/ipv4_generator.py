import random
import subprocess


def generateOctet1():
    octet = int(255*random.random())
    while str(octet) == '10':
        octet = int(255*random.random())
    return octet

def generateOctet2(octet1: int):
    blackListNumbers172 = [x for x in range(32)]
    blackListNumbers192 = 168
    blackListNumbers169 = 254
    octet = int(255*random.random())

    if octet1 == 172:        
        while octet < 32:
            octet = int(255*random.random())
    elif octet1 == 192:
        while octet == 168:
            octet = int(255*random.random())
    elif octet1 == 169:
        while octet == 254:
            octet = int(255*random.random())
    return octet

def generateOctet():
    octet = int(255*random.random())
    return octet
    

#Private addresses 10.0.0.0/8, 172.16.0.0-172.31.255.255/12, 192.168.0.0/16, 169.254.0.0/16
PRIVATE_ADDRESSES_OCTECT1 = ['10']
PRIVATE_ADDRESSES_OCTECT2 = ['172','192','169']
PRIVATE_ADDRESSES_OCTECT3 = ['192.168','169.254']


def generateDomain():
    octet1 = generateOctet1()
    octet2 = generateOctet2(octet1)
    octet3 = generateOctet()
    octet4 = generateOctet()

    ip_addr = [octet1,octet2,octet3,octet4]

    ip_addrStr = ".".join([str(octect) for octect in ip_addr])

    print(ip_addrStr)
    #ip_addrStr = "178.162.39.224"

    command1 = 'nslookup '+ip_addrStr+' ^| findstr "Name: "'
    command2 = 'for /f "tokens=2" %i in '
    command3 = "('"+command1+"') do echo %i"

    command = command2+command3
    #print(command)
    try:
        domain = subprocess.check_output(command, shell=True, text=True)
        start = domain[1:].find("\n")
        domain = domain[start:].strip()
        return domain
    except subprocess.CalledProcessError as e:
        print("can't resolve ip")
        return ""

domainName = ""
while domainName == "":
    domainName = generateDomain()

print(domainName)
