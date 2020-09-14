import mysql.connector
import sys


def genCursor(config):
    try:
        return mysql.connector.connect(**config).cursor(buffered=True)
    except mysql.connector.connection.errors:
        print("Cannot connect to server!!")
        exit(1)
