#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports
import os
from ..utils.utils import *

#We Mainly Utilize this module to fight for randomness to adjust program to alsr to certain position.

class Processer:
 
    code_text = ""
    code_readonly = ""
    code_readwrite = ""
    stack = ""
    
    def __init__(self, pid):

        self.pid          = pid
        self.proc         = "/proc/" + str(self.pid) + "/%s"
        self.exeutable    = self.proc % "exe"
        self.pwd          = self.proc % "cwd"
        self.cmdline_path = self.proc % "cmdline"
        self.map_path     = self.proc % "maps"
        self.mem_path     = self.proc % "mem"

        #init parsing procedure..
        self._init()

    def _init(self):

        self.get_exe_parameters()
        self.parse_mapping()


    def get_exe_parameters(self):
        
        self.exeutable = os.readlink(self.exeutable)
        self.pwd       = os.readlink(self.pwd)
        self.args      = open(self.cmdline_path).read().split("\x00")
        #in case pwntools inits with shell=True;
        #you'd better use shell=False(default option)
        if self.args[0] == "/bin/sh" and self.args[1] == "-c":
            self.args = self.args[2].split(" ")

    def parse_mapping(self):

        #extract information really needed for now!
        #proc_segs is a tuple, containing:
        #(addr_start, addr_end, permission, filename) for current usage.
        self.proc_segs = {}
        counter = 0
        mapping_fp = open(self.map_path, "rb")
        map_content = mapping_fp.read()
        mapping_fp.close()
        for map_seg in map_content.split("\n"):
            if len(map_seg) < 8:
                #that's impossible or vacant..;
                continue
            seg0 = map_seg.split(" ")
            addr = seg0[0].split("-")
            addr_start = addr[0].strip() #care: hex value instr;
            addr_end   = addr[1].strip() #care: hex value instr;
            permission = seg0[1].strip() #care: r-xp ; r--p ; rw-p;
            filename   = seg0[-1].strip()#care: file loaded in memory;
#            print "%s : %s : %s : %s" % (addr_start, addr_end, 
#                                         permission, filename)
            #adding counter to count mmaping segs..
            seg_key = filename.strip("[").strip("]").split("/")[-1].strip()
            if len(seg_key) == 0:
                seg_key = "mmap_" + str(counter)
                counter += 1
            self.proc_segs[seg_key] = (addr_start, addr_end, 
                                       permission, filename)
        dbg_info(self.proc_segs)
        

    #facilities...
    def pick_mem(self, offset, length):

        fp_ = open(self.mem_path , 'rb')
        fp_.seek(offset)
        content = fp_.read(length)
        return content

        
        

#interface
def mem(pid):

    pid = get_pid(pid)
    p = Processer(pid)
    return p

