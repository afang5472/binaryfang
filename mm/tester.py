#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

#We Utilize this module to fight for randomness to adjust program to alsr to certain position.

class Processer:
 
    code_text = ""
    code_readonly = ""
    code_readwrite = ""
    stack = ""
    
    def __init__(self, maps, pid):

        self.maps = maps
        self.pid = pid
        self.try_read(self.pid)

    def try_read(self, pid):

        print self.maps
        fp_ = open('/proc/' + pid + '/mem')
        fp_.seek(0x400000)
        content = fp_.read()

def mem_reader(pid):

    pid = str(pid)
    pid = pid.strip("[").strip("]")
    fp = open("/proc/" + pid + "/maps")
    maps = fp.read()
    p = Processer(maps, pid)
    fp.close()


