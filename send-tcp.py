#!/usr/bin/env python2.7

import socket

TCP_IP = '10.29.45.3'
TCP_PORT = 1180
BUFFER_SIZE = 1024
MESSAGE = "Hello, world!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
while True:
    data = ""
    data = s.recv(BUFFER_SIZE)
    print "recieved data:", data

s.close()
