import socket
import time

#need a script for the raspberry pi and the controller 

HOST = "192.168.1.100"
PORT = 5000

def start_run():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.send("START".encode())

    client.close()

start_run()