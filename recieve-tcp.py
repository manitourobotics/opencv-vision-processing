#!/usr/bin/env python2.7

import socket
import time
import traceback
import sys

# Do not use bind with localhost as the address -- The port will
#   not be opened to outside IPs
TCP_IP = ''
TCP_PORT  = 1180
BUFFER_SIZE = 20 # Norally 1024, but we want a fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT)) # still needs to be a tupple
s.listen(1)

while True:
    conn, addr = s.accept() # Accept any connections. 
    # Reaccept if connection lost

    while True:
        print 'Connection address:', addr
        try:
            # Send test data
            conn.send("foo\n")
            conn.send("bar\n")
        except socket.error, e: 
            # If the client closes the connection, don't quit and
            #   look for a new one
            print "socket error({0}): {1}. Listening for new connection" \
                    .format(e.errno, e.strerror)
            conn.close()
            break
        time.sleep(1) # Do I need a wait?

conn.close()
