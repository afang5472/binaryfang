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
        self.mem_path = "/proc/" + self.pid + "/mem"
        self.try_read(self.pid)

    def pick_mem(self, offset, length):

        print self.maps
        fp_ = open(self.mem_path , 'rb')
        fp_.seek(offset)
        content = fp_.read(length)
        return content.encode('hex')

def mem(pid):

    pid = str(pid)
    pid = pid.strip("[").strip("]")
    fp = open("/proc/" + pid + "/maps", 'r')
    maps = fp.read()
    p = Processer(maps, pid)
    fp.close()

