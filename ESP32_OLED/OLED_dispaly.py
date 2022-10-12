import serial
import psutil
from time import sleep
import socket
sleeptime = 0.5
logfile = "jp2091"

def socket_start():
    global sock
    sock = socket.socket()
    host = "192.168.137.32"
    port = 8080
    sock.connect((host, port))
    print("Connected . . .")

def socket_send(st):
    sock.sendall(bytes("$%s" % st, encoding="utf-8"))
    print("sent:%s"%st)


def bytes_received():
    traffic = psutil.net_io_counters(pernic=False, nowrap=False)
    return traffic.bytes_recv

def SerialConnect():
    try:
        global ser
        ser = serial.Serial('COM8', 9600, timeout=200)
        if ser.is_open == True:
            print("Connected")
    except:
        print("fonction SerialConnect, Check if you had connect to port or not.")

def Get_cpu_usage():
    cpu_usage = psutil.cpu_percent()
    return  cpu_usage

def VPN_connection_checker(file_name = logfile + '.nordvpn.com.udp.log'):
    path = "C://Users//66405//OpenVPN//log//" + file_name
    fo = open(path,encoding="utf-8")
    info_list = []
    for line in fo:
        line = line.replace("\n", "")
        info_list.append(line.strip(","))
    fo.close()
    if info_list[-1].find('CONNECTED,SUCCESS') != -1:
        return True
    elif info_list[-1].find('Control Channel:') != -1:
        return True
    elif info_list[-1].find('AEAD Decrypt error:') != -1:
        return True
    else:
        return False

def serial_input(A = str):
    str(A)
    input_intiger = A
    bytes_converter_variable = str(input_intiger)
    bstr = bytes( bytes_converter_variable, encoding="utf8")
    ser.write(bstr)
    #print("\ryou had write:{}".format(bstr),end="")   #Print what you had write


def LCD_str_inputmaker(input_str = ""):
    str_lis = input_str.split('&')
    output_str = ""
    for i in str_lis:
        formed_str =  i.ljust(20)
        output_str = output_str +'\n' + formed_str
    return output_str



def main():
    socket_start()
    SerialConnect()
    byte_sum = 0
    old_bytes_received = bytes_received()
    while True:
        VPN = ""
        cpu_usage = Get_cpu_usage()
        serial_input_v = int(cpu_usage/20)
        byte_sum  = byte_sum + (bytes_received() - old_bytes_received)
        byte_add_kb = (((bytes_received() - old_bytes_received)*(1/sleeptime))/800)*3
        int_byte_add_kb = int(byte_add_kb)
        try:
            if VPN_connection_checker() == True:
                socket_send(LCD_str_inputmaker("CPU:{:.0f}% RAM:{:.0f}%  &{}:{}".format(cpu_usage, psutil.virtual_memory().percent,logfile.upper(), str(int_byte_add_kb)+'Kbps' if int_byte_add_kb < 1000 else str(int_byte_add_kb/500)[0:4]+'Mbps')))
        except:
            socket_send(LCD_str_inputmaker("CPU:{:.0f}% RAM:{:.0f}%  &Network:{}".format(cpu_usage,psutil.virtual_memory().percent, str(int_byte_add_kb)+'Kbps' if int_byte_add_kb < 1000 else str(int_byte_add_kb/500)[0:4]+'Mbps')))
            old_bytes_received = bytes_received()
            sleep(sleeptime)

if __name__ == '__main__':
    main()


