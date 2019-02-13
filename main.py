#!/usr/bin/python

import sys
import sqlite3
from sqlite3 import Error
import socket

HOST = 'localhost'
PORT = 11211

class Memcache():

    _create_table_sql = (
        'CREATE TABLE IF NOT EXISTS cache '
        '('
        '  key TEXT PRIMARY KEY,'
        '  val BLOB'
        ')'
    )
    _get_sql = 'SELECT val FROM cache WHERE key = ?'
    _del_sql = 'DELETE FROM cache WHERE key = ?'
    _add_sql = 'INSERT INTO cache (key, val) VALUES (?, ?)'

    db_connection = None
    socket_connection = None

    def __init__(self, db_file):
        self.create_connection(db_file)
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
            self.socket_connection, addr = s.accept()
            with self.socket_connection:
                print('Connected by', addr)
                while True:
                    data = self.socket_connection.recv(1024)
                    if not data:
                        break
                    data = data.decode('utf-8').split()
                    self.process_command(data)

    def process_command(self, data):
        if data[0] == 'get':
            self.get(data)
        elif data[0] == 'set':
            self.set(data)
        elif data[0] == 'delete':
            self.delete(data)
        else:
            self.socket_connection.send('Invalid command.\n')
            return None

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        print('creating db connection')
        try:
            self.db_connection = sqlite3.connect(db_file)
            self.db_connection.execute(self._create_table_sql)
            print('Ran the create table')
        except Error as e:
            print(e)

        return None

    def get(self, data):
        # Retrieve a property from cache
        if len(data) > 1:
            key = data[1]
            for row in self.db_connection.execute(self._get_sql, (key,)):
                self.socket_connection.send(row[0].encode('utf-8'))
            return
        self.socket_connection.send('Invalid get command'.encode('utf-8'))

    def delete(self, key):
        # Delete property from cache
        if len(data) > 1:
            key = data[1]
            self.socket_connection.send('issued delete {key}\n'.format(key=key).encode('utf-8'))
            return
        self.socket_connection.send('Invalid delete command'.encode('utf-8'))

    def set(self, data):
        # Set a property in cache
        if len(data) > 2:
            key = data[1]
            value = data[2]
            with self.db_connection as conn:
                try:
                    conn.execute(self._add_sql, (key, value))
                except sqlite3.IntegrityError:
                    # call the update method as fallback
                    print('Attempting to set an existing key {k}. Falling back to update method.')
                    pass
                return
        self.socket_connection.send('Invalid set command'.encode('utf-8'))

    def show(self):
        # Show all values from cache
        print('show all data')
        return

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        cache = Memcache()
        cache.show()
        sys.exit(1)
    elif len(sys.argv) == 3 and sys.argv[1] == 'serve':
        cache = Memcache(sys.argv[2])
