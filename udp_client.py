#!/usr/bin/env python2
# SIMPLE UDP CLIENT

import socket

host = '127.0.0.1'
port = 80

# create socket obj
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data
client.sendto("AAABBBCCC", (host, port))

# receive data
data, addr = client.recvfrom(4096)

print data

