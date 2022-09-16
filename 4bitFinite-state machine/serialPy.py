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
        time.sleep(0.01)

    def test(self):
        for i in [2, 3, 4, 5]:
            print(i)
            num = "${}".format(i)
            num = num.rstrip()

        for i in [2, 3, 4, 5]:
            num = "^{}".format(i)
            num = num.rstrip()

        for i in [2, 3, 4, 5]:
            print(i)
            num = "${}".format(i)
            num = num.rstrip()

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
        elif state == 4:
            self.four()
        elif state == 5:
            self.five()
        elif state == 6:
            self.six()
        elif state == 7:
            self.seven()
        elif state == 8:
            self.eight()





    def clearAllbits(self):
        for i in [2, 3, 4, 5]:
            num = "${}".format(i)
            num = num.rstrip()
            value = UNO_Serial1.write_read(num)

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
            value = UNO_Serial1.write_read(num)
    
    def two(self):
        for i in [3]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial1.write_read(num)

    def three(self):
        for i in [2,3]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial1.write_read(num)
    
    def four(self):
        for i in [4]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial1.write_read(num)

    def five(self):
        for i in [2,4]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial1.write_read(num)

    def six(self):
        for i in [3,4]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial1.write_read(num)

    def seven(self):
        for i in [2,3,4]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial1.write_read(num)

    def eight(self):
        for i in [2,3,4,5]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = UNO_Serial1.write_read(num)

def main():
    global UNO_Serial1
    UNO_Serial1 = UNO_Serial()
    UNO_Serial1.test()
    fouritFinite1 = fouritFinite()
    i = 1
    while True:
        print(i)
        fouritFinite1.switch(i)
        time.sleep(1)
        i = i+1
        if i == 9:
            i = 0


    

if __name__ == "__main__":
    main()