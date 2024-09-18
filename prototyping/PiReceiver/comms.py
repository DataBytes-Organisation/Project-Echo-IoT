# Abstracted comms component


import socket
import re

def regex_split(address):
    delims = "://" , ":"
    regex = '|'.join(map(re.escape, delims))
    protocol, ip, port = re.split(regex, address)

    return protocol, ip, port

def receive_connect(bind):

    # Simple sockets require the IP/port in a different format to other protocols.  Split the endpoint address
    _, ip, port = regex_split(bind)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(('', int(port)))

    return sock

def receive_message(server):

    data, addr = server.recvfrom(1024)

    return data


def send_message(endpoint, message):

    # Simple sockets require the IP/port in a different format to other protocols.  Split the endpoint address
    _, ip, port = regex_split(endpoint)

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message, (ip, int(port)))

    return True