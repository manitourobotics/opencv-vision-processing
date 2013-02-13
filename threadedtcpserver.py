import pickle
import time
import traceback
import socket
import threading 

class ConnectionThread( threading.Thread ):


    horizontal_alignment = -1000.0
    previous_horizontal_alignment = horizontal_alignment

    HORIZONTAL_ALIGNMENT=1
    HORIZONTAL_ALIGNMENT_=2
    TARGET_HIGH=1
    TARGET_MIDDLE=2
    TARGET_LOW=3

    def run(self):
        
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.bind( ('', 1180) )
        s.listen(2) # I want another listener for testing

        while True:
            conn, addr = s.accept()

            while True:
                print "conn addr:", addr
                try:

                    # don't send duplicate information
                    if( self.previous_horizontal_alignment != self.horizontal_alignment ):
                        information = str(self.HORIZONTAL_ALIGNMENT) + ":" + str(self.horizontal_alignment) + "\n"
                        conn.send(information)
                        print "information sent"
                    elif(self.previous_horizontal_alignment == self.horizontal_alignment):
                        previous_horizontal_alignment = self.horizontal_alignment  
                        print "duplicate information"
                    else:
                        print "error "
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
        connThread.horizontal_alignment = i
        i+=1
    

