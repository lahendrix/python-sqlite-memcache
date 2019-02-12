#!/usr/bin/python

import sqlite3
from sqlite3 import Error

class Memcache():

    create_sql = (
        'CREATE TABLE IF NOT EXISTS cache '
        '('
        '  key TEXT PRIMARY KEY,'
        '  val BLOB,'
        ')'
    )
    get_sql = 'SELECT val FROM cache WHERE key = ?'
    del_sql = 'DELETE FROM cache WHERE key = ?'
    set_sql = 'REPLACE INTO cache (key, val) VALUES (?, ?)'
    add_sql = 'INSERT INTO cache (key, val) VALUES (?, ?)'

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
        return