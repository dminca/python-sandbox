#!/usr/bin/env python2
# SIMPLE TCP CLIENT

import socket

host = 'www.google.com'
port = 80

# create socket obj
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect
client.connect((host, port))

# send data
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receive data
response = client.recv(4096)

print response

