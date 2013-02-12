import pickle
import time
import traceback
import socket
import threading 

class ConnectionThread( threading.Thread ):


    distance = -1000.0
    previous_distance = distance

    DISTANCE_PACKET=1

    def run(self):
        
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.bind( ('', 1180) )
        s.listen(1)

        while True:
            conn, addr = s.accept()

            while True:
                print "conn addr:", addr
                try:

                    # don't send duplicate information
                    if( self.previous_distance != self.distance ):
                        conn.send( self.DISTANCE_PACKET + str(self.distance) + "\n")
                    previous_distance = self.distance  
                except socket.error:
                    print "socket err"
                    traceback.print_exc()
                    conn.close()
                    break
                time.sleep(0.05) 
            time.sleep(1)



if __name__ == '__main__':
    connThread = ConnectionThread()
    connThread.start()
    i = 0
    while True:
        time.sleep(1)
        connThread.distance = i
        i+=1
    

