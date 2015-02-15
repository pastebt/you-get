#! /usr/bin/python3

import os
import sys
from multiprocess import Pipe, Queue, Process

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


def work():
    url = "http://www.dailymotion.com/video/k65xg3tOFvWf7a9CtyR"
    url = "http://www.dailymotion.com/video/k24yMzJwTk5oW29DIrD"
    url = "http://www.dailymotion.com/video/koWwt2hrjlB7S89Io00"
    #download_main(any_download, None, [url], None,
    #          output_dir="/home/maye/workspace/github/you-get/")


class Worker(object):
    def __init__(self, que):
        self.reader, sender = Pipe(False)
        self.proc = Process(target=self.run, args=[que, sender])

    def run(self, que, sender):
        que.get()
        url = pick_url()
        work()


class Manager(object):
    def __init__(self, que, wnum=2):
        self.works = [0] * wnum
        self.que = que
        self.running = True
        for i in range(wnum):
            self.works[i] = Worker(self.que)

    def run(self):
        while self.running:
            select(self.works.reader.fileno)
