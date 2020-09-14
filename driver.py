import mysql.connector
from sqlgen.utilities.utility import prettyprint
import argparse
import sqlite3

import sys


config = {
    "port": '4000',
    'database': 'test'
}

parser = argparse.ArgumentParser()

parser.add_argument('-D', '--driver', type=str,
                    choices=['mysql', 'mariadb', 'tidb', 'postgres', 'sqlite', 'timescale'],
                    help='database server')
parser.add_argument('-H', '--host', type=str,
                    help='host')
parser.add_argument('-P', '--port', type=str,
                    help='port')
parser.add_argument('-u', '--user', type=str,
                    help='the user to connect the database')
parser.add_argument('-p', '--password',
                    help='password')
parser.add_argument('-d', '--database', type=str,
                    help='use the given database. Need file path if connecting to sqlite.')

args = parser.parse_args()

if len(sys.argv) < 2:
    prettyprint('!', "You must give an argument. See the help message")
    print('\n\n')
    parser.print_help()
    exit(0)

global driver

if args.driver is not None:
    driver = args.driver
else:
    driver = 'mysql'


try:
    if driver == 'mysql':
        prettyprint('*', 'Use MySQL connector')
        cnx = mysql.connector.connect(**config, buffered=True, autocommit=True, consume_results=True)
        cu = cnx.cursor()
    elif driver == 'sqlite':
        prettyprint('*', 'Use SQLite connector')
        if args.database is None:
            prettyprint('!', 'I need a database name. Try `-d` or `--database`')
            exit(1)
        con = 'file:{}?mode=rwc'
        import sqlite3

        cnx = sqlite3.connect(con.format(args.database), uri=True)
        cu = cnx.cursor()
    else:
        prettyprint('>', 'I cannot connect to the given server because it is not implemented. '
                         'Please try another one instead.')
        exit(1)

    prettyprint(".", "All right, let's start!")
    print("Nothing to do, exit")

except Exception:
    pass


