#! /usr/bin/python3

import os
import sys
import select
from multiprocessing import Pipe, Queue, Process


_srcdir = '../src/'
if getattr(sys, 'frozen', False):
    # The application is frozen
    _filepath = os.path.dirname(os.path.realpath(sys.executable))
else:
    # The application is not frozen
    # Change this bit to match where you store your data files:
    _filepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(_filepath, _srcdir))


from you_get.common import any_download, download_main
from db import pick_url, update_filename, set_flag


class WFP(object):
    def __init__(self, p):
        self.p = p

    def write(self, dat):
        self.p.send(dat)

    def flush(self):
        pass


def work(uobj):
    download_main(any_download, None, [uobj.url], None,
                  output_dir="../")


class Worker(Process):
    def __init__(self, que):
        Process.__init__(self)
        self.que = que
        self.mod = None
        self.reader, self.sender = Pipe(False)

    def fileno(self):   # help for select
        return self.reader.fileno()

    def run(self):
        sys.stdout = WFP(self.sender)
        while True:
            mid = self.que.get()
            if mid is None:
                break
            uobj = pick_url(mid)
            self.sender.send("Process mid=%d Start" % uobj.rowid)
            try:
                work(uobj)
            except:
                self.sender.send("Process mid=%d Fail" % uobj.rowid)
            else:
                self.sender.send("Process mid=%d Stop" % uobj.rowid)


class Manager(Process):
    def __init__(self, wnum=2):
        Process.__init__(self)
        self.m2w = self.s2m = Queue()
        self.works = [0] * wnum
        for i in range(wnum):
            self.works[i] = Worker(self.m2w)
            self.works[i].start()

    """
Video Site: bilibili.com
Title:      【BD‧1080P】【高分剧情】鸟人-飞鸟侠 2014【中文字幕】
Type:       Flash video (video/x-flv)
Size:       3410.85 MiB (3576536465 Bytes)

Downloading 【BD‧1080P】【高分剧情】鸟人-飞鸟侠 2014【中文字幕】.flv ...
  0.7% ( 22.2/3410.9MB) [#
    """
    def run(self):
        while True:
            #select(self.works.reader.fileno)
            #self.handle_worker(self.works[0])
            rl, wl, xl = select.select(self.works, [], [], 5)
            for wk in rl:
                self.handle_worker(wk)

    def handle_worker(self, wk):
        dats = wk.reader.recv()
        for dat in dats.split('\n'):
            print("[" + dat + "]")
            if dat.startswith("Process ") and "mid" in dat:
                dd = dat.split()
                mid = dd[1][4:]
                act = dd[2].lower()
                set_flag(mid, act)
                wk.mid = mid if act == 'start' else None
            elif dat.startswith("Downloading "):
                print(dat)
                print("mid=[%s]" % wk.mid)
                if wk.mid is not None:
                    update_filename(wk.mid, dat[12:-4])
