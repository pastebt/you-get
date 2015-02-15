#! /usr/bin/python3

import os
import sys
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
from db import pick_url


class WFP(object):
    def __init__(self, p):
        self.p = p

    def write(self, dat):
        self.p.send(dat)

    def flush(self):
        pass


def work(uobj):
    #url = "http://www.dailymotion.com/video/k65xg3tOFvWf7a9CtyR"
    #url = "http://www.dailymotion.com/video/k24yMzJwTk5oW29DIrD"
    #url = "http://www.dailymotion.com/video/koWwt2hrjlB7S89Io00"
    download_main(any_download, None, [uobj.url], None,
              output_dir="/home/maye/workspace/github/you-get/")


class Worker(Process):
    def __init__(self, que):
        Process.__init__(self)
        self.que = que
        self.reader, self.sender = Pipe(False)

    def run(self):
        sys.stdout = WFP(self.sender)
        while True:
            mid = self.que.get()
            if mid is None:
                break
            uobj = pick_url(mid)
            self.sender.send("Process mid=%d Start" % uobj.rowid)
            work(uobj)
            self.sender.send("Process mid=%d Stop" % uobj.rowid)


class Manager(Process):
    def __init__(self, wnum=1):
        Process.__init__(self)
        self.m2w = self.s2m = Queue()
        self.wnum = wnum

        self.works = [0] * self.wnum
        for i in range(self.wnum):
            self.works[i] = Worker(self.m2w)
        self.works[0].start()

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
            dat = self.works[0].reader.recv()
            print("[" + dat + "]")
            if dat.startswith("Downloading ") or dat.startswith("Process "):
                print(dat)
