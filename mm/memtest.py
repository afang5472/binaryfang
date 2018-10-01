#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:

# imports

#We Utilize this module to fight for randomness to adjust program to alsr to certain position.

class Processer:
 
    code_text = ""
    code_readonly = ""
    code_readwrite = ""
    stack = ""
    
    def __init__(self, pid):

        self.pid = pid
        self.prefix = "/proc/" + self.pid
        self.maps = self.prefix + "/maps"
        self.mem  = self.prefix + "/mem"
        self.bin  = self.prefix + "/exe"
        self.cwd  = self.prefix + "/cwd"
        self.map_fp = open(self.maps, "rb")
        self.mem_fp = open(self.mem, "rb")

    def pick_mem(self, offset, length):

        self.mem_fp.seek(offset)
        content = self.mem_fp.read(length)
        return content
    
    def test(self):

        print self.pid
        print self.prefix
        print self.maps
        print self.bin
        print self.map_fp

def mm(pid):

    pid = str(pid)
    p = Processer(pid)
    return p

