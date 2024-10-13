import serial
import psutil
from time import sleep
import socket
import json

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

def send_socket_data(data):
    """
    Send data through the socket connection in JSON format.
    
    Args:
    - data (dict): The data to be sent.

    Returns True if successful, False otherwise.
    """
    try:
        json_data = json.dumps(data)  # Convert dictionary to JSON
        socket_conn.sendall(bytes(f"${json_data}", encoding="utf-8"))
        print(f"Sent: {json_data}")
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
            byte_rate_bps = ((current_bytes_received - previous_bytes_received) * (1 / SLEEP_TIME)) * 8
            network_speed_bps = byte_rate_bps

            temp = 25  # Simulate a temperature read (you can pass actual values if available)
            
            # Prepare data in JSON format
            data = {
                "cpu": cpu_usage,
                "ram": ram_usage,
                "temp": temp,
                "network": network_speed_bps
            }

            # Check socket connection and send data
            if not is_socket_connected():
                print("Socket disconnected.")
                reconnect_socket()

            if not send_socket_data(data):
                reconnect_socket()

            # Update the old bytes received value
            previous_bytes_received = current_bytes_received
            sleep(SLEEP_TIME)
        
        except Exception as e:
            print(f"Error in main loop: {e}")
            sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
