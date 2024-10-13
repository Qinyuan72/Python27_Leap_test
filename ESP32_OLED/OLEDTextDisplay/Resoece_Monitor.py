"""
System Monitoring with Socket and Serial Connection

This program connects to a remote server via socket, gathers system information
like CPU, RAM, and network speed, and sends this data through a serial connection.
Additionally, it generates an ASCII art display for visualizing the status on an OLED screen.

Author: Qinyuan Liu
Electronic Engineering
Copyright © 12/10/2024
"""

import serial
import psutil
from time import sleep
import socket

# Configuration variables
SLEEP_TIME = 0.5  # Time interval for each update
LOG_FILE = "jp2091"
HOST = "192.168.31.155"
PORT = 8080

def start_socket():
    """
    Establish a socket connection to the server.
    Returns True if connection is successful, False otherwise.
    """
    try:
        global socket_conn
        socket_conn = socket.socket()
        socket_conn.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
    except socket.error as e:
        print(f"Socket connection error: {e}")
        return False
    return True

def socket_send(st):
    """
    Send data through the socket connection.
    
    Args:
    - st (str): The data to be sent.

    Returns True if successful, False otherwise.
    """
    try:
        socket_conn.sendall(bytes(f"${st}", encoding="utf-8"))
        print(f"Sent: {st}")
    except (socket.error, OSError) as e:
        print(f"Socket send error: {e}")
        return False
    return True


def is_socket_connected():
    """
    Check if the socket connection is still active by sending an empty packet.
    Returns True if the socket is active, False otherwise.
    """
    try:
        socket_conn.sendall(b'')
    except (socket.error, OSError):
        return False
    return True

def reconnect_socket():
    """
    Attempt to reconnect the socket in case of disconnection.
    """
    print("Attempting to reconnect to socket...")
    while not start_socket():
        print("Reconnection failed. Retrying in 5 seconds...")
        sleep(5)
    print("Reconnected successfully!")

def get_bytes_received():
    """
    Return the total number of bytes received by the network interface.
    """
    return psutil.net_io_counters(pernic=False, nowrap=False).bytes_recv

def connect_serial():
    """
    Establish a serial connection on COM8 with a baud rate of 9600.
    """
    try:
        global serial_conn
        serial_conn = serial.Serial('COM8', 9600, timeout=200)
        if serial_conn.is_open:
            print("Serial connected")
    except serial.SerialException as e:
        print(f"Serial connection error: {e}")

def get_cpu_usage():
    """
    Get the current CPU usage as a percentage.
    """
    return psutil.cpu_percent()

def check_vpn_connection(log_file=LOG_FILE + '.nordvpn.com.udp.log'):
    """
    Check VPN connection status by reading the log file.
    Returns True if VPN is connected, False otherwise.

    Args:
    - log_file (str): The VPN log file name.
    """
    try:
        log_path = f"C://Users//66405//OpenVPN//log//{log_file}"
        with open(log_path, encoding="utf-8") as log:
            info_list = [line.strip(",").replace("\n", "") for line in log]
        
        if 'CONNECTED,SUCCESS' in info_list[-1] or 'Control Channel:' in info_list[-1] or 'AEAD Decrypt error:' in info_list[-1]:
            return True
        return False
    except FileNotFoundError:
        print(f"VPN log file not found: {log_file}")
        return False

def write_serial_data(data):
    """
    Write data to the serial port.

    Args:
    - data (str): The string to be written to the serial port.
    """
    try:
        serial_conn.write(bytes(data, encoding="utf8"))
    except serial.SerialException as e:
        print(f"Serial write error: {e}")

def format_LCD_display(input_str=""):
    """
    Format string for LCD display, splitting into lines of 16 characters.
    
    Args:
    - input_str (str): The string to be formatted for the display.

    Returns a formatted string.
    """
    lines = input_str.split('&')
    return '\n'.join([line.ljust(16) for line in lines])

def generate_ascii_art_display(temp, cpu, ram, network_speed):
    """
    Generate a simple ASCII art display for RAM, CPU, temperature, and network speed.
    
    Args:
    - temp (float): Temperature value.
    - cpu (float): CPU usage percentage.
    - ram (float): RAM usage percentage.
    - network_speed (str): Network speed in Kbps or Mbps.

    Returns a formatted ASCII art string, ensuring lines fit on the display.
    """
    temp_bar = "#" * int((temp / 100) * 10)  # Temperature bar scaled to 10 chars max
    cpu_bar = "#" * int((cpu / 100) * 10)    # CPU usage bar scaled to 10 chars max
    ram_bar = "#" * int((ram / 100) * 10)    # RAM usage bar scaled to 10 chars max

    return (
        f"RAM:  [{ram_bar.ljust(10)}]\n"
        f"      {ram:.1f}%\n"
        f"CPU:  [{cpu_bar.ljust(10)}]\n"
        f"      {cpu:.1f}%\n"
        f"TEMP: {temp:.1f}C\n"               # Ensure TEMP is on its own line
        f"NET:  {network_speed}"             # NET on a separate line
    )



def main():
    """
    Main function to monitor system status, send data over serial and socket,
    and display status on an OLED screen.
    """
    # Initialize socket connection
    if not start_socket():
        reconnect_socket()

    connect_serial()
    previous_bytes_received = get_bytes_received()

    while True:
        try:
            cpu_usage = get_cpu_usage()
            ram_usage = psutil.virtual_memory().percent
            current_bytes_received = get_bytes_received()
            byte_rate_kbps = (((current_bytes_received - previous_bytes_received) * (1 / SLEEP_TIME)) / 800) * 3
            network_speed = f"{int(byte_rate_kbps)}Kbps" if byte_rate_kbps < 1000 else f"{byte_rate_kbps / 500:.2f}Mbps"

            temp = 25  # Simulate a temperature read (you can pass actual values if available)
            vpn_status = check_vpn_connection()

            if vpn_status:
                display_str = generate_ascii_art_display(temp, cpu_usage, ram_usage, network_speed)
            else:
                display_str = generate_ascii_art_display(temp, cpu_usage, ram_usage, network_speed)

            # Check socket connection and send data
            if not is_socket_connected():
                print("Socket disconnected.")
                reconnect_socket()

            if not socket_send(display_str):
                reconnect_socket()

            # Update the old bytes received value
            previous_bytes_received = current_bytes_received
            sleep(SLEEP_TIME)
        
        except Exception as e:
            print(f"Error in main loop: {e}")
            sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
