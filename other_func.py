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

def beautify(text, symbol, side, desired_len=0):

    if side == 'top':
        return str(symbol * (len(text) if not desired_len else desired_len)) + '\n' + text
    elif side == 'bottom':
        return text + '\n' + str(symbol * (len(text) if not desired_len else desired_len))



ascii_logo = r"""
         ____
        |    |
        |____|
       _|____|_               _                     _
        /  ee`.     _ _  ___ | |_  ___   _ _  ___ _| |_
      .<     __O   | '_>/ . \| . \/ . \ | '_><_> | | |
     /\ \.-.' \    |_|  \___/|___/\___/ |_|  <___| |_|
    J  `.|`.\/ \                  
    | |_.|  | | |
     \__.'`.|-' /
     L   /|o`--'\ 
     |  /\/\/\   \           
     J /      `.__\
     |/         /  \     
      \\\     .'`.  `.                                            .'
    ____)_/\_(____`.  `-._______________________________________.'/
   (___._/  \_.___) `-.________________________________________.-'
"""