import socket
import time
import datetime


HEADERSIZE = 8

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    client_socket, address = s.accept()
    print(f'Connection from {address} has ben established!')

    msg = "Welcome to the broker!"
    msg = f'{len(msg):<{HEADERSIZE}}' + msg

    client_socket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(3)
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        msg = f'The time is: {current_time}'
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        client_socket.send(bytes(msg, "utf-8"))
