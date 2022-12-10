import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))


import socket, Leap
from time import sleep

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    frameInfo = ''
    accumulatorFloat = 0.0
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

    def accumulator(self,newFloat):
        self.accumulatorFloat += self.accumulatorFloat - newFloat
        return self.accumulatorFloat

    def on_frame(self,controller):
        frame = controller.frame()
        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        
        
        for tool in frame.tools:

            print "  Tool id: %d, position: %s, direction: %s" % (tool.id, tool.tip_position, tool.direction)

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                    self.frameInfo = "circle %i&clockwise" % (round(circle.progress,0))
                    #self.accumulator(circle.progress)
                else:
                    clockwiseness = "counterclockwise"
                    self.frameInfo = "circle %i&Conterclockwise" % (round(circle.progress,0))

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START: previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI
                

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (gesture.id, self.state_names[gesture.state],circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (gesture.id, self.state_names[gesture.state],swipe.position, swipe.direction, swipe.speed)
                self.frameInfo = "swipe"

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                print "  Key Tap id: %d, %s, position: %s, direction: %s" % (gesture.id, self.state_names[gesture.state],keytap.position, keytap.direction )
                self.frameInfo = "keytap"

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (gesture.id, self.state_names[gesture.state],screentap.position, screentap.direction )
                self.frameInfo = "Screen Tap"
        #espSocket8266.socket_send(espSocket8266.LCD_str_inputmaker(self.frameInfo))



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
            print("espSocket.sent:%s"%st)
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
    #espSocket8266 = espSocket(espSocketConfig=('192.168.31.154',8080))#This two line is necessary to initialize the PSM object.
    #espSocket8266.espSocket_start()                                        #//

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
