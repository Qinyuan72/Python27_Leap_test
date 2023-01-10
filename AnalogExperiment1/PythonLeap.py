################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time, os, serial
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    valTest = 0

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

    def on_frame(self, controller):
        time.sleep(0.1)
        os.system('cls')
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)
        
            val = hand.palm_position[1]
            val = int((val-100)/2)
            if (val >= 0 and val <=255):
                if val != self.valTest:
                    UNO_Serial1.write(UNO_Serial1.inputFormart(val))
                    self.valTest = val
            else:
                print "Out of range val = %s" % val 
            print ('PWM value: %s' % val)
            dataArry = UNO_Serial1.format(UNO_Serial1.arduino.read(100))
            print(dataArry)
            UNO_Serial1.writeData(dataArry)

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (gesture.id, self.state_names[gesture.state],swipe.position, swipe.direction, swipe.speed)
                self.frameInfo = "swipe"
                self.plotData()
                time.sleep(1)


    def plotData(self):
        f.close
        os.system('python AnalogExperiment1\Test\plot.py')
        pass

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

class UNO_Serial:
    def __init__(self):
        self.arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
        self.arduino.readline()

    def write(self, x):
        self.arduino.write(bytes(x))
        time.sleep(0.01)

    def inputFormart(self, inputInt):
        outputStr = '{}\n'.format(inputInt)
        return outputStr

    def format(self,str):
        write = False
        arrBuffer = str.split('S')
        return arrBuffer[1:len(arrBuffer)-1]

    def writeData(self,arrData):
        for i in arrData:
            f.write('%s\n'%i)
        f.close


def main():
    # Create a sample listener and controller
    global f
    f = open('AnalogExperiment1//Test//1N4148.csv','a+')
    global UNO_Serial1
    UNO_Serial1 = UNO_Serial()
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
