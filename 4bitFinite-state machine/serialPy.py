from asyncio import sleep
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
        self.arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
        print (self.arduino.readline())

    def write_read(self,x):
        self.arduino.write(bytes(x, 'ASCII'))
        time.sleep(0.1)
        data = self.arduino.readline()
        return data

    def test(self):
        for i in [2, 3, 4, 5]:
            print(i)
            num = "${}".format(i)
            num = num.rstrip()
            value = self.write_read(num)
            print(value)  # printing the value
            time.sleep(0.5)

        for i in [2, 3, 4, 5]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = self.write_read(num)
            print(value)  # printing the value
            time.sleep(0.5)


class fouritFinite:

    def switch(self,state):
        self.clearAllbits()
        if state == 0:
            self.zero()
        elif state == 1:
            self.one()
        elif state == 2:
            self.two()
        elif state == 3:
            self.three()

    def clearAllbits(self):
        for i in [2, 3, 4, 5]:
            num = "${}".format(i)
            num = num.rstrip()
            value = UNO_Serial.write_read(num)
            print(value)  # printing the value
            time.sleep(0.5)

    def zero(self):
        '''
        for i in []:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial.write_read(num)
            print(value)  # printing the value
            time.sleep(0.2)
        '''
        pass

    def one(self):
        for i in [2]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial.write_read(num)
            print(value)  # printing the value
            time.sleep(0.2)
    
    def two(self):
        for i in [3]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial.write_read(num)
            print(value)  # printing the value
            time.sleep(0.2)

    def three(self):
        for i in [2,3]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial.write_read(num)
            print(value)  # printing the value
            time.sleep(0.2)

def main():
    global UNO_Serial
    UNO_Serial = UNO_Serial()
    UNO_Serial.test()

    

if __name__ == "__main__":
    main()