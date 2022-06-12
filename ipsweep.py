from re import match
import sys
from math import pow
import socket

def getValidIpAddresses(ip: str, onBits: int):
    ipSegments = ip.split('.')
    newIpSegment = list()
    index = 0
    while onBits > 0:
        if not onBits >= 8:
            onBits = 0
            newIpSegment.append("0")
            for k,v in enumerate(ipSegments):
                if not v == "1":
                    ipSegments[k] = "0"
            break
        onBits -= 8
        index += 1
        newIpSegment.append(ipSegments[index])
        ipSegments[index] = "1"
    return

def TryConnections(ip: str):
    target = socket.gethostbyname(ip)
    #Add banner
    #print(f"{'-'*50}\nScanning target {target}\nTime started: {str(datetime.now())}\n{'-'*50}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, 80))
        if result == 0:
            print(f"IP: Device at {target}")
    except KeyboardInterrupt:
        print("\nExiting")
        sys.exit()
    except socket.gaierror:
        print("Failed to resolve hostname.")
        sys.exit()
    except socket.error:
        print("failed to connect to server.")
        sys.exit()
    finally:
        s.close()

def run() -> None:
    if len(sys.argv) != 2:
        print("Invalid no. arguments.")
        print("Syntax: python3 ipsweep.py 192.168.68.0/24")
        return
    pattern = "(([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\/([0-9]{1,2}))"
    result = match(pattern, sys.argv[1])
    if not result:
        print("Invalid formate for arguments.")
        print("Syntax: python3 ipsweep.py 192.168.68.0/24")
        return
    template = ".".join(sys.argv[1].split('/')[0].split('.')[:-1])
    [TryConnections(f'{template}.{num}') for num in range(0,255)]
    

if __name__ == "__main__":
    run()