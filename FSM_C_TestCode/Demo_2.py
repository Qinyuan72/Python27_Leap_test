from asyncio import sleep
from asyncore import loop
from pickle import TRUE
import serial
import time

'''
def write_read(x):
    arduino.write(bytes(x, 'ASCII'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


while True:
    for i in [2, 3, 4, 5]:
        num = "${}".format(i)
        num = num.rstrip()
        value = write_read(num)
        print(value)  # printing the value
        time.sleep(0.5)

    for i in [2, 3, 4, 5]:
        num = "^{}".format(i)
        num = num.rstrip()
        value = write_read(num)
        print(value)  # printing the value
        time.sleep(0.5)
'''


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
        loopBool = TRUE
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
        loopBool = TRUE
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
