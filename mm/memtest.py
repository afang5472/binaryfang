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

    def pick_mem(self, offset, length):

        fp_ = open(self.mem_path , 'rb')
        fp_.seek(offset)
        content = fp_.read(length)
        return content

def mem(pid):

    pid = str(pid)
    pid = pid.strip("[").strip("]")
    p = Processer(pid)
    return p

