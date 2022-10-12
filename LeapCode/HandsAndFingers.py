import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

    |
import socket
from time import sleep

import Leap

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self,controller):
        frame = controller.frame()
        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        framInfo = ''
        handType = ''
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
            print "  %s, id %d, position: %s" % (handType, hand.id, hand.palm_position) #Hand position 
            for finger in hand.fingers:

                print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                    self.finger_names[finger.type],
                    finger.id,
                    finger.length,
                    finger.width)

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    print "      Bone: %s, start: %s, end: %s, direction: %s" % (self.bone_names[bone.type],bone.prev_joint,bone.next_joint,bone.direction)
        framInfo = "%s&fingers: %d" % (handType, len(frame.fingers))

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
