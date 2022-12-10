import serial
import time

def ConsoleInput():
    inputInt = input("Number range form 0 -255: ")
    inputStr = '{}\n'.format(inputInt)
    arduino.write(bytes(inputStr,'ASCII'))

def loop(limite):
    i = 0
    while (i <= limite):
        i += 1
        for o in range(0,255):
            inputStr = '{}\n'.format(o)
            arduino.write(bytes(inputStr,'ASCII'))
            #time.sleep(0.001)
            print(inputStr)

        for o in range(255,0,-1):
            inputStr = '{}\n'.format(o)
            arduino.write(bytes(inputStr,'ASCII'))
            #time.sleep(0.001)
            print(inputStr)

def main():
    global arduino
    arduino = serial.Serial(port='COM3', baudrate=115200, timeout=100)
    arduino.write(bytes('200\n', 'ASCII'))
    loop(1000)


if __name__ == "__main__":
    main()


