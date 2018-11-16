#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports
import os
import ctypes
#We Utilize this module to attach to remote program to control its' data&code&registers .


class debugger:
 
    #reserved staffs
    code_text = ""
    code_readonly = ""
    code_readwrite = ""
    stack = ""
    
    def __init__(self, pid, mappings):

        self.pid          = pid
        self.mappings     = mappings
        self._init()

    def _init(self):

        #show parameters right.
        print "[*]pid: " + self.pid
        print "[*]mappings: "
        for x in self.mappings:
            print x



#interface
def dbg(pid, mappings):

    pid = str(pid)
    pid = pid.strip("[").strip("]")
    p = debugger(pid, mappings)
    return p

