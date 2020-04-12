import os
import random

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def invalid_inp():
    print("\n ERROR: invalid input")
    input(" ENTER to try again > ")


def random_name():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    name = ''

    for _ in range(7):
        name += random.choice(chars)
    return name


def beautify(text, symbol, side=0, desired_len=0):

    txt = ''
    if side == 'top' or not side:
        txt += str(symbol * (len(text) if not desired_len else desired_len)) + '\n'
        if side:
            return txt + text

    if side == 'bottom' or not side:
        txt += text + '\n' + str(symbol * (len(text) if not desired_len else desired_len))
        if side:
            return txt

    return txt

ascii_logo = r"""
 ______     ______   __  __     __     __     ______     ______     ______    
/\  ___\   /\  == \ /\ \_\ \   /\ \  _ \ \   /\  __ \   /\  == \   /\  ___\   
\ \___  \  \ \  _-/ \ \____ \  \ \ \/ ".\ \  \ \  __ \  \ \  __<   \ \  __\   
 \/\_____\  \ \_\    \/\_____\  \ \__/".~\_\  \ \_\ \_\  \ \_\ \_\  \ \_____\ 
  \/_____/   \/_/     \/_____/   \/_/   \/_/   \/_/\/_/   \/_/ /_/   \/_____/ 
                                                                                                                                                                      
"""

ascii_cmd = r"""
 ______     ______     __    __     __    __     ______     __   __     _____     ______    
/\  ___\   /\  __ \   /\ "-./  \   /\ "-./  \   /\  __ \   /\ "-.\ \   /\  __-.  /\  ___\   
\ \ \____  \ \ \/\ \  \ \ \-./\ \  \ \ \-./\ \  \ \  __ \  \ \ \-.  \  \ \ \/\ \ \ \___  \  
 \ \_____\  \ \_____\  \ \_\ \ \_\  \ \_\ \ \_\  \ \_\ \_\  \ \_\\"\_\  \ \____-  \/\_____\ 
  \/_____/   \/_____/   \/_/  \/_/   \/_/  \/_/   \/_/\/_/   \/_/ \/_/   \/____/   \/_____/                                                                                      
"""