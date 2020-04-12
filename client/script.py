import socket
import cv2

HOST = socket.gethostname()
PORT = 55555
DATA_PORT = 44444
HDR_SIZE = 1024

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.connect((HOST, PORT))
data_socket.connect((HOST, DATA_PORT))


while True:
    cmd = main_socket.recv(HDR_SIZE).decode("utf-8")
    print(cmd)

    if cmd == 'take_pic':
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        camera.release()