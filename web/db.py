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
            url text,           -- movie url
            name text,          -- movie name
            mime text,          -- mime from remote
            size bigint,        -- movie file size
            path text,          -- movie local file path
            updt datetime,      -- when the url be submitted
            bgdt datetime,      -- when the url start download
            eddt datetime,      -- when the url finished download
            prog real,          -- progress, xx.x%
            prio tinyint,       -- downlaod priority
            flag tinyint        -- status, WAIT, WORKING, DONE
        )''')


class UOBJ(object):
    def __init__(self, dats=[]):
        for dat in dats:
            setattr(self, dat[0], dat[1])

    def __str__(self):
        return str(self.__dict__)


def add_one_url(url, title=""):
    with SDB() as c:
        c.execute("insert into aviurl (url, name, updt) "
                  "values (?, ?, datetime('now', 'localtime'))",
                  (url, title))


def query_urls():
    with SDB() as c:
        urls = c.execute("select rowid, * from aviurl")
        desc = [x[0] for x in c.description]
        # have to finish this in "with" scope
        #ret = [dict(zip(desc, url)) for url in urls]
        ret = [UOBJ(zip(desc, url)) for url in urls]
    return ret


def dump_urls():
    for uobj in query_urls():
        print(uobj)


def usage():
    print('URL DB utility')
    print('Usage:', sys.argv[0], "-l")
    print('    -l  list all url in DB')
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        usage()

    if sys.argv[1] == '-l':
        dump_urls()
    else:
        usage()


if __name__ == '__main__':
    main()
