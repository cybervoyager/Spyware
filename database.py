import sqlite3


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