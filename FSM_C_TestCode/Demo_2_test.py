from traceback import print_list
import serial
import time


class UNO_Serial:
    def __init__(self):
        self.arduino = serial.Serial(port='COM10', baudrate=115200, timeout=.1)
        self.arduino.readline()

    def write(self, x):
        self.arduino.write(bytes(x, 'ASCII'))
        time.sleep(0.01)

    def inputFormart(self, inputInt):
        inputInt = chr(inputInt+48)
        outputStr = "${}".format(inputInt)
        return outputStr


class Test:
    def terminalInput():
        testinput = 0
        loopBool = True
        while loopBool:
            try:
                testinput = int(input("Accept number form 1-16 to set case: "))
                testinput = UNO_Serial1.inputFormart(testinput)
            except ValueError:
                print("Illegal input")
            UNO_Serial1.write(testinput)

            if (input("Anykey to reset /n to exit ") == '/n'):
                loopBool = False
            UNO_Serial1.write(UNO_Serial1.inputFormart(17))

    def loopAllBitTest():
        print("loopAllBitTest")
        loopBool = True
        while loopBool:
            for i in range(1, 16):
                UNO_Serial1.write(UNO_Serial1.inputFormart(i))
                time.sleep(0.5)
                UNO_Serial1.write(UNO_Serial1.inputFormart(17))
                time.sleep(0.5)


def main():
    global UNO_Serial1
    UNO_Serial1 = UNO_Serial()
    Test.terminalInput()
    Test.loopAllBitTest()


if __name__ == "__main__":
    main()
