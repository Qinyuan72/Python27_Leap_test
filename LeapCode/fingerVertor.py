################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import serial
import Leap
import sys
import thread
import time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from math import acos, degrees
import os


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
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):

        time.sleep(0.1)
        os.system('cls')
        arr = [False, False, False, False]
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        if len(frame.hands) == 2:

            hand = frame.hands.rightmost

            print"Right most hand"
            for finger in hand.fingers:
                if self.finger_names[finger.type] == "Index":
                    print "    %s finger, id: %d, length: %fmm, width: %fmm" % (self.finger_names[finger.type], finger.id, finger.length, finger.width)

                    bone = finger.bone(3)
                    print "      Bone: %s, direction: %s" % (self.bone_names[bone.type], degrees(acos(bone.direction[2])))
                    if degrees(acos(bone.direction[2])) > 45:
                        arr[1] = True

                if self.finger_names[finger.type] == "Middle":
                    print "    %s finger, id: %d, length: %fmm, width: %fmm" % (self.finger_names[finger.type], finger.id, finger.length, finger.width)

                    bone = finger.bone(3)
                    print "      Bone: %s, direction: %s" % (self.bone_names[bone.type], degrees(acos(bone.direction[2])))
                    if degrees(acos(bone.direction[2])) > 45:
                        arr[0] = True

            hand = frame.hands.leftmost

            print"Left most hand"
            for finger in hand.fingers:
                if self.finger_names[finger.type] == "Index":
                    print "    %s finger, id: %d, length: %fmm, width: %fmm" % (self.finger_names[finger.type], finger.id, finger.length, finger.width)

                    bone = finger.bone(3)
                    print "      Bone: %s, direction: %s" % (self.bone_names[bone.type], degrees(acos(bone.direction[2])))
                    if degrees(acos(bone.direction[2])) > 45:
                        arr[2] = True

                if self.finger_names[finger.type] == "Middle":
                    print "    %s finger, id: %d, length: %fmm, width: %fmm" % (self.finger_names[finger.type], finger.id, finger.length, finger.width)

                    bone = finger.bone(3)
                    print "      Bone: %s, direction: %s" % (self.bone_names[bone.type], degrees(acos(bone.direction[2])))
                    if degrees(acos(bone.direction[2])) > 45:
                        arr[3] = True
        b = arr
        val = reduce(lambda byte, bit: byte*2 + bit, b, 0)

        print val

        if val != self.valTest:
            UNO_Serial1.write(UNO_Serial1.inputFormart(17))
            UNO_Serial1.write(UNO_Serial1.inputFormart(val))
            self.valTest = val
            


class UNO_Serial:
    def __init__(self):
        self.arduino = serial.Serial(port='COM10', baudrate=115200, timeout=.1)
        self.arduino.readline()

    def write(self, x):
        self.arduino.write(bytes(x))
        time.sleep(0.01)

    def inputFormart(self, inputInt):
        inputInt = chr(inputInt+48)
        outputStr = "${}".format(inputInt)
        return outputStr

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"


def main():
    # Create a sample listener and controller
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
