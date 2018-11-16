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
from ..utils.utils import *
from ..mm.memtest import *

#We Utilize this module to attach to remote program to control its' data&code&registers .

class debugger:
 
    #reserved staffs
    code_text = ""
    code_readonly = ""
    code_readwrite = ""
    stack = ""
    
    def __init__(self, pid, mappings):

        #initiates with pid && maps
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
def dbg(pid):

    pid = get_pid(pid)
    mem_mgr = mem(pid)
    p = debugger(pid, mem_mgr.proc_segs)
    return p

