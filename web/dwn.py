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
    def __init__(self, who, out, mid=0):
        self.out = out
        self.mid = mid
        self.left = ""
        self.who = who

    def write(self, dat):
        self.left = self.left + dat
        if self.left[-1] in '\r\n' or len(self.left) > 200:
            self.out.put({"who": self.who, "mid": self.mid, "dat": self.left})
            self.left = ""

    def flush(self):
        pass


def work(uobj):
    download_main(any_download, None, [uobj.url], None,
                  output_dir="../")


class Worker(Process):
    def __init__(self, s2m, m2w):
        Process.__init__(self)
        self.s2m, self.m2w = s2m, m2w

    def run(self):
        while True:
            mid = self.m2w.get()
            if mid is None:
                break
            sys.stdout = WFP("worker", self.s2m, mid)
            sys.stderr = WFP("error", self.s2m, mid)
            uobj = pick_url(mid)
            print("Process mid=%d Start" % uobj.rowid)
            try:
                work(uobj)
            except:
                print("Process mid=%d Fail" % uobj.rowid)
            else:
                print("Process mid=%d Stop" % uobj.rowid)


class Manager(Process):
    def __init__(self, wnum=2):
        Process.__init__(self)
        self.s2m = Queue()  # message Manager receive from worker and svr
        self.m2w = Queue()  # message send to works
        self.works = [0] * wnum
        for i in range(wnum):
            self.works[i] = Worker(self.s2m, self.m2w)
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
            msg = self.s2m.get()
            who = msg.get('who')
            if who == 'worker':
                self.handle_mid(msg['mid'], msg['dat'])
            elif who == 'svr':
                self.m2w.put(msg['mid'])
            elif who == 'error':
                sys.stderr.write(msg['dat'])   # FIXME
                sys.stderr.write("\n")
            else:
                sys.stderr.write("Unknow msg:\n")
                sys.stderr.write(msg)
                sys.stderr.write("\n")

    def handle_mid(self, mid, dat):
        print(dat)
        if dat.startswith("Process "):
            dd = dat.split()
            act = dd[2].lower()
            print("mid=%s, act=%s" % (mid, act))
            set_flag(mid, act)
        elif dat.startswith("Downloading "):
            print("mid=[%s]" % mid)
            update_filename(mid, dat[12:-4])
