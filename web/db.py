#! /usr/bin/python3

import sys
import sqlite3


dbfile = "url_info.db"


def init_db():
    global dbfile

    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute('''
        create table if not exists stocks (
            url text,
            title text,
            size int,
            prog real,
            done bool,
            wait bool
        )''')
    conn.commit()
    c.close()
    conn.close()


def usage():
    print('URL DB utility')
    print('Usage:', sys.argv[0], "-l")
    print('    -l  list all url in DB')
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        usage()

    if sys.argv[1] == '-l':
        list_all()
    else:
        usage()


if __name__ == '__main__':
    main()
