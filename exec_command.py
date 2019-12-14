from other_func import *
import threading, time


class ExecuteCommands(object):

    def __init__(self, victim_data):
        self.victim_data = victim_data
        self.switch = True
        self.thread = True
        self.clear_sc = True

        self.run_cmd = {
            'webcam_snap': ['Take (x) pictures every (y) seconds', self.webcam_snap],
            'back': ['Go back to victim selection', self.back]
        }

    def pick_command(self):
        while self.switch:

            if self.clear_sc:
                clear_screen()

                for cmd in self.run_cmd:
                    print(f"{cmd} = {self.run_cmd[cmd][0]}")

                if self.thread:
                    self.thread = False
                    input_thread = threading.Thread(target=self.get_input)
                    input_thread.start()

                self.clear_sc = False


    def get_input(self):
        while self.switch:
            command = input("\n >>> ")

            if command in self.run_cmd:
                output = self.run_cmd[command][1]()

                if output == 'back':
                    self.switch = False

            self.clear_sc = True
            time.sleep(0.1)

    def webcam_snap(self):
        print("Webcam")

    def back(self):
        return 'back'