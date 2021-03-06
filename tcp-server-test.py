#!/usr/bin/env python2.7

import socket
import time
import traceback
import sys

if __name__ == '__main__':
    # Do not use bind with localhost as the address -- The port will
    #   not be opened to outside IPs
    TCP_IP = ''
    TCP_PORT  = 1180

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT)) # still needs to be a tupple
    s.listen(1) # Only l isten for one connection max

    while True:
        try:
            conn, addr = s.accept() # Accept any connections. 
            # Reaccept if connection lost

            while True:
                print 'Connection address:', addr
                try:
                    # Send test data
                    conn.send("foo\n")
                    conn.send("bar\n")
                except socket.error: 
                    # If the client closes the connection, don't quit and
                    #   look for a new one
                    traceback.print_exc()
                    conn.close()
                    break
                time.sleep(1) # Do I need a wait? -- rapid sucession of sends else

        except KeyboardInterrupt:
            conn.close()
            s.shutdown(socket.SHUT_RDWR)
