#!/usr/bin/python

import sys
import sqlite3
from sqlite3 import Error
import socket

HOST = 'localhost'
PORT = 11211

class Memcache():

    create_table_sql = (
        'CREATE TABLE IF NOT EXISTS cache '
        '('
        '  key TEXT PRIMARY KEY,'
        '  val BLOB'
        ')'
    )
    get_sql = 'SELECT val FROM cache WHERE key = ?'
    del_sql = 'DELETE FROM cache WHERE key = ?'
    set_sql = 'REPLACE INTO cache (key, val) VALUES (?, ?)'
    add_sql = 'INSERT INTO cache (key, val) VALUES (?, ?)'

    connection = None

    def create_server(self):
        """ create a server that listens on
            port 11211
        :return: None
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            self.connection = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return None

    def get(self, key):
        # Retrieve a property from cache
        return

    def delete(self, key):
        # Delete property from cache
        return

    def set(self, key, value):
        # Set a property in cache
        return

    def show(self):
        # Show all values from cache
        print('show all data')
        return

if __name__ == '__main__':
    if sys.argv[0] != 'show':
        cache = Memcache()
        cache.show()
        sys.exit(1)
