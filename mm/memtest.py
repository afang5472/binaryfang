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
    
    def __init__(self, pid):

        self.pid = pid
        self.map_path = "/proc/" + self.pid + "/maps"
        self.mem_path = "/proc/" + self.pid + "/mem"
        self.fp_map = open(self.map_path, "rb")
        self.fp_mem = open(self.mem_path, "rb")
        self.maps = self.fp_map.read()

    def pick_mem(self, offset, length):

        self.fp_mem.seek(offset)
        content = self.fp_mem.read(length)
        return content

def mm(pid):

    pid = str(pid)
    pid = pid.strip("[").strip("]")
    p = Processer(pid)
    return p

