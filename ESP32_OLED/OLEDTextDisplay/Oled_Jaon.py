import serial
import psutil
from time import sleep
import socket
import json
import logging

# Configuration variables
SLEEP_TIME = 0.5  # Time interval for each update
LOG_FILE = "jp2091"
HOST = "192.168.31.155"
PORT = 8080

# Configure logging
logging.basicConfig(filename='system_monitor.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def start_socket():
    """
    Establish a socket connection to the server.
    Returns True if connection is successful, False otherwise.
    """
    try:
        global socket_conn
        socket_conn = socket.socket()
        socket_conn.connect((HOST, PORT))
        logging.info(f"Connected to server at {HOST}:{PORT}")
    except socket.error as e:
        logging.error(f"Socket connection error: {e}")
        return False
    return True

def send_socket_data(data):
    """
    Send data through the socket connection.
    
    Args:
    - data (str): The data to be sent.

    Returns True if successful, False otherwise.
    """
    try:
        socket_conn.sendall(bytes(f"${data}", encoding="utf-8"))
        logging.info(f"Sent: {data}")
    except (socket.error, OSError) as e:
        logging.error(f"Socket send error: {e}")
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
    logging.warning("Attempting to reconnect to socket...")
    while not start_socket():
        logging.warning("Reconnection failed. Retrying in 5 seconds...")
        sleep(5)
    logging.info("Reconnected successfully!")

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
            logging.info("Serial connected")
    except serial.SerialException as e:
        logging.error(f"Serial connection error: {e}")

def get_cpu_usage():
    """
    Get the current CPU usage as a percentage.
    """
    return psutil.cpu_percent()

def write_serial_data(data):
    """
    Write data to the serial port.

    Args:
    - data (str): The string to be written to the serial port.
    """
    try:
        serial_conn.write(bytes(data, encoding="utf8"))
    except serial.SerialException as e:
        logging.error(f"Serial write error: {e}")

def prepare_json_payload(cpu, ram, temp, network_speed):
    """
    Prepare JSON payload to send to Arduino.

    Args:
    - cpu (float): CPU usage.
    - ram (float): RAM usage.
    - temp (float): Temperature.
    - network_speed (str): Network speed.

    Returns a JSON string.
    """
    payload = {
        "cpu": cpu,
        "ram": ram,
        "temp": temp,
        "network_speed": network_speed
    }
    return json.dumps(payload)

def main():
    """
    Main function to monitor system status, send data over serial and socket,
    and display status on an OLED screen.
    """
    logging.info("Starting system monitor...")
    
    # Initialize socket connection
    if not start_socket():
        reconnect_socket()

    connect_serial()
    previous_bytes_received = get_bytes_received()

    logging.info("Entering main loop...")
    
    while True:
        try:
            cpu_usage = get_cpu_usage()
            ram_usage = psutil.virtual_memory().percent
            current_bytes_received = get_bytes_received()
            byte_rate_kbps = (((current_bytes_received - previous_bytes_received) * (1 / SLEEP_TIME)) / 800) * 3
            network_speed = f"{int(byte_rate_kbps)}Kbps" if byte_rate_kbps < 1000 else f"{byte_rate_kbps / 500:.2f}Mbps"

            temp = 25  # Simulate a temperature read (you can pass actual values if available)

            # Prepare JSON payload
            json_payload = prepare_json_payload(cpu_usage, ram_usage, temp, network_speed)

            # Log payload to make sure it is built correctly
            logging.info(f"Payload: {json_payload}")

            # Check socket connection and send data
            if not is_socket_connected():
                logging.warning("Socket disconnected.")
                reconnect_socket()

            if not send_socket_data(json_payload):
                reconnect_socket()

            # Update the old bytes received value
            previous_bytes_received = current_bytes_received
            sleep(SLEEP_TIME)
        
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
