import socket

HOST = "127.0.0.1"  #insert host IP address here RPMI computer
PORT = 5000

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    while True:
        cmd = input("Command (START/STOP/PING/EXIT): ")

        client.send(cmd.encode())

        if cmd == "PING":
            print(client.recv(1024).decode())

        if cmd == "EXIT":
            break

    client.close()

run_client()