#!/usr/bin/python

def encode(msg):
    return (msg + "\n").encode('utf-8')

def format_row(row):
    return '{:<10} | {:<10}'.format(*row)
