import socket
import threading
from utils import get_latest_csv 
from monitor import tail_csv

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

            print("Waiting for CSV...")

            while True:
                latest = get_latest_csv(RPMI_FOLDER)

                if latest:
                    print("Found file:", latest)

                    running_flag["running"] = True

                    threading.Thread(
                        target=tail_csv,
                        args=(latest, running_flag),
                        daemon=True
                    ).start()

                    break

        elif data == "STOP":
            running_flag["running"] = False
            print("Stopped")

        elif data == "PING":
            conn.send("ALIVE".encode())

    conn.close()