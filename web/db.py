#! /usr/bin/python3

import sys
import sqlite3


dbfile = "url_info.db"


class SDB(object):
    def __enter__(self):
        global dbfile
        self.conn = sqlite3.connect(dbfile)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


def init_db():
    with SDB() as c:
        c.execute('''
        create table if not exists aviurl (
            url text,
            title text,
            size int,
            `when` datetime,
            prog real,
            done bool,
            wait bool
        )''')


def add_one_url(url, title=""):
    with SDB() as c:
        c.execute("insert into aviurl (url, title) values (?, ?)",
                  (url, title))


def dump_urls():
    with SDB() as c:
        urls = c.execute("select * from aviurl")
        for url in urls:
            print(url)


def usage():
    print('URL DB utility')
    print('Usage:', sys.argv[0], "-l")
    print('    -l  list all url in DB')
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        usage()

    if sys.argv[1] == '-l':
        #list_all()
        dump_urls()
    else:
        usage()


if __name__ == '__main__':
    main()
