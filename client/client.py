import socket

HOST = socket.gethostname()
PORT = 55555
DATA_PORT = 44444

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.connect((HOST, PORT))
data_socket.connect((HOST, DATA_PORT))

while True:
    x = input("+++")
    if x == 'q':
        break