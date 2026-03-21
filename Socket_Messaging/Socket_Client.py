import socket

HOST = "192.168.1.100"
PORT = 5000

def run_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    while True:
        cmd = input("Enter command (START / STOP / PING / EXIT): ")

        client.send(cmd.encode())

        if cmd == "PING":
            response = client.recv(1024).decode()
            print("Server:", response)

        if cmd == "EXIT":
            break

    client.close()

run_client()