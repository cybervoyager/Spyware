import os, random


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