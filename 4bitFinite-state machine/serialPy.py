# Importing Libraries
from msilib.schema import Class
import serial
import time

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)


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
        time.sleep(0.2)

    for i in [2, 3, 4, 5]:
        num = "^{}".format(i)
        num = num.rstrip()
        value = write_read(num)
        print(value)  # printing the value
        time.sleep(0.2)


class UNO_Serial:
    def UNO_Serial():
        arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

    def write_read(x):
        arduino.write(bytes(x, 'ASCII'))
        time.sleep(0.05)
        data = arduino.readline()
        return data

    def test():
        while True:
        for i in [2, 3, 4, 5]:
            num = "${}".format(i)
            num = num.rstrip()
            value = write_read(num)
            print(value)  # printing the value
            time.sleep(0.2)

        for i in [2, 3, 4, 5]:
            num = "^{}".format(i)
            num = num.rstrip()
            value = write_read(num)
            print(value)  # printing the value
            time.sleep(0.2)

class fouritFinite:
    