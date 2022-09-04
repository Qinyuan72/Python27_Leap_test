import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))


import socket
from time import sleep

import Leap

class SampleListener(Leap.Listener):
    
    def on_connect(self, controller):
        print "Connected"

    def on_frame(self,controller):
        frame = controller.frame()
        framInfo = "hands: %d, &fingers: %d" % (len(frame.hands), len(frame.fingers))
        #print framInfo
        espSocket8266.socket_send(espSocket8266.LCD_str_inputmaker(framInfo))



class espSocket:
    sock=0
    stCompar = ''
    def __init__(self,espSocketConfig):
        self.espSocketConfig = espSocketConfig
    
    def espSocket_start(self):
        self.sock = socket.socket()
        print('Networkconfig: '+str(self.espSocketConfig)+' Connecting...')
        try:
            self.sock.connect((self.espSocketConfig))
            print("Socket connection successful")
        except:
            print("Socket connection failed")
    
    def socket_send(self,st):
        if st != self.stCompar:
            self.sock.sendall(bytes("$%s" % st))
            print("sent:%s"%st)
            self.stCompar = st
        
    def LCD_str_inputmaker(self,input_str = ""):
        str_lis = input_str.split('&')
        output_str = ""
        for i in str_lis:
            formed_str =  i.ljust(40)
            output_str = output_str + formed_str
        return output_str
            
def main():
    global espSocket8266
    espSocket8266 = espSocket(espSocketConfig=('192.168.31.154',8080))#This two line is necessary to initialize the PSM object.
    espSocket8266.espSocket_start()                                        #//

    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
