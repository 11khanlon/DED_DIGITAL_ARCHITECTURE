import os
import socket
import threading
from Socket_Messaging.RPMIandClient.utils import get_latest_csv 
from Socket_Messaging.RPMIandClient.monitor import tail_csv
import time

HOST = "0.0.0.0" #insert host IP address here. RPMI computer 
PORT = 5000      #create port for custom protocol
RPMI_FOLDER = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\Mazak"   #insert actual folder path where RPMI saves CSV files

running_flag = {"running": False}  #set global variable to false, not running yet

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print("Server waiting...")

    conn, addr = server.accept()
    print("Connected:", addr)

    while True:
        data = conn.recv(1024).decode().strip()

        if not data:
            break

        print("Received:", data)

        if data == "START" and not running_flag["running"]:

            print("START received")

            start_time = time.time()
            running_flag["running"] = True

            print("Waiting for NEW CSV after START...")

            while True:

                latest = get_latest_csv(RPMI_FOLDER)

                if latest is None:
                    time.sleep(0.2)
                    continue

                file_time = os.path.getmtime(latest)

                if file_time >= start_time:

                    print("Monitoring file:", latest)

                    threading.Thread(
                        target=tail_csv,
                        args=(latest, running_flag, conn),
                        daemon=True
                    ).start()

                    break

        elif data == "STOP":
            running_flag["running"] = False
            print("Stopped")

        elif data == "PING":
            conn.send("ALIVE".encode())

    conn.close()