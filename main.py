#!/usr/bin/python

import sys
import sqlite3
from sqlite3 import Error
import socket
from utils import encode, format_row

HOST = 'localhost'
PORT = 11211

class Memcache():

    _create_table_sql = (
        'CREATE TABLE IF NOT EXISTS cache '
        '('
        ' key TEXT PRIMARY KEY,'
        ' val BLOB,'
        ' exptime FLOAT' # ignored for now
        ')'
    )
    _get_sql = 'SELECT val FROM cache WHERE key = ?'
    _del_sql = 'DELETE FROM cache WHERE key = ?'
    _add_sql = 'INSERT INTO cache (key, val) VALUES (?, ?)'
    _show_sql = 'SELECT key, val from cache'

    db_conn = None
    socket_conn = None

    def __init__(self, db_file, start_server):
        self.create_connection(db_file)
        if start_server:
            self.create_server()

    def create_server(self):
        """ create a server that listens on
            port 11211
        :return: None
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            print('server started at {host}:{port}'.format(host=HOST, port=PORT))
            s.listen(5)
            self.socket_conn, addr = s.accept()
            with self.socket_conn:
                print('Connected by', addr)
                while True:
                    data = self.socket_conn.recv(1024)
                    if not data:
                        break
                    self.process_command(data)

    def process_command(self, data):
        """ Parses incoming socket data and detmines
            which command to execute
        :param data: list
        :return:
        """
        data = data.decode('utf-8').split()
        if data[0] == 'get':
            self.get(data)
        elif data[0] == 'set':
            self.set(data)
        elif data[0] == 'delete':
            self.delete(data)
        else:
            self.socket_conn.send(encode('Invalid command: {command}'.format(command=data[0])))
            return None

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            self.db_conn = sqlite3.connect(db_file)
            self.db_conn.execute(self._create_table_sql)
        except Error as e:
            print(e)

        return None

    def get(self, data):
        # Retrieve a property from cache
        if len(data) > 1:
            key = data[1]
            for row in self.db_conn.execute(self._get_sql, (key,)):
                self.socket_conn.send(encode(row[0]))
            return
        self.socket_conn.send(encode('Proper usage: get <key>'))

    def delete(self, data):
        # Delete property from cache
        if len(data) > 1:
            key = data[1]
            with self.db_conn as conn:
                conn.execute(self._del_sql, (key,))
                return
        self.socket_conn.send(encode('Proper usage: delete <key>'))

    def set(self, data):
        # Set a property in cache
        if len(data) > 2:
            key = data[1]
            value = data[2]
            with self.db_conn as conn:
                try:
                    conn.execute(self._add_sql, (key, value))
                except sqlite3.IntegrityError:
                    pass
                return
        self.socket_conn.send(encode('Proper usage: set <key> <val>'))

    def show(self):
        # Show all values from cache
        separator = '-' * 20
        print(format_row(("Key", "Value")))
        print(separator)
        with self.db_conn as conn:
            for row in conn.execute(self._show_sql):
                print(format_row(row))
        return

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        cache = Memcache(sys.argv[2], False)
        cache.show()
        sys.exit(1)
    elif len(sys.argv) == 3 and sys.argv[1] == 'serve':
        cache = Memcache(sys.argv[2], True)
