#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:

# imports
import os
import ctypes
from ..utils.utils import *
from ..mm.memtest import *
import time

#We Utilize this module to attach to remote program to control its' data&code&registers .

PTRACE_TRACEME    = 0 
PTRACE_ATTACH     = 0x10 
PTRACE_GETREGS    = 0xc 
PTRACE_DETACH     = 0x11 
PTRACE_SINGLESTEP = 0x9 
PTRACE_CONT       = 0x7

class UserRegsStruct(ctypes.Structure):
    _fields_ = [
        ("r15", ctypes.c_ulonglong),
        ("r14", ctypes.c_ulonglong),
        ("r13", ctypes.c_ulonglong),
        ("r12", ctypes.c_ulonglong),
        ("rbp", ctypes.c_ulonglong),
        ("rbx", ctypes.c_ulonglong),
        ("r11", ctypes.c_ulonglong),
        ("r10", ctypes.c_ulonglong),
        ("r9", ctypes.c_ulonglong),
        ("r8", ctypes.c_ulonglong),
        ("rax", ctypes.c_ulonglong),
        ("rcx", ctypes.c_ulonglong),
        ("rdx", ctypes.c_ulonglong),
        ("rsi", ctypes.c_ulonglong),
        ("rdi", ctypes.c_ulonglong),
        ("orig_eax", ctypes.c_ulonglong),
        ("rip", ctypes.c_ulonglong),
        ("cs", ctypes.c_ulonglong),
        ("eflags", ctypes.c_ulonglong),
        ("rsp", ctypes.c_ulonglong),
        ("ss", ctypes.c_ulonglong),
        ("fs_base", ctypes.c_ulonglong),
        ("gs_base", ctypes.c_ulonglong),
        ("ds", ctypes.c_ulonglong),
        ("es", ctypes.c_ulonglong),
        ("fs", ctypes.c_ulonglong),
        ("gs", ctypes.c_ulonglong),
    ]

class debugger:
 
    #reserved staffs
    code_text = ""
    code_readonly = ""
    code_readwrite = ""
    stack = ""
    
    def __init__(self, pid, mappings):

        #initiates with pid && maps
        #pid should be convert to a size_t
        self.pid          = int(pid)
        self.mappings     = mappings
        self._init()

    def get_libc_handle(self):

        self.libc = ctypes.CDLL("libc.so.6")

    def _init(self):
        
        #load libc && initiate user-regs.

        self.get_libc_handle()
        self.regs = UserRegsStruct()
        self.reserved_regs = UserRegsStruct() #reserve when alter

        #Currently attach a target to be debugged.
        #show parameters right.

        dbg_info("dbg: " + str(self.mappings))
        #attach..!
        #test get some mapping sections , ready for breaking.
        self.get_mappingof("libc")

        #ptrace attach
        self.raw_attach()

        #attacher entering region
        cnt = 0
        while 1: 
            _, status = os.wait()
            #automatic debugging procedure fill-in here.
            cnt += 1
            self.getregs()
            self.cont()
            self.detach()
            break
   
#todo: loading with symbol resolver.

    def raw_attach(self):

        assert self.libc, "[*]libc instance is None"
        if self.libc.ptrace((PTRACE_ATTACH), self.pid, 0, 0) != 0:
            self.libc.perror("ptrace attach error: ")
        return 

    def cont(self):
        #continue execution
        assert self.libc, "[*]libc instance is None"
        if self.libc.ptrace((PTRACE_CONT), self.pid, 0, 0) != 0:
            self.libc.perror("continue exec error: ")
        return 
        
    def getregs(self):
        #get current regs values
        assert self.libc, "[*]libc instance is None"
        if self.libc.ptrace((PTRACE_GETREGS), self.pid, 0, ctypes.byref(self.regs)) != 0:
            self.libc.perror("get regs error: ")

        dbg_info('rip = {:016X}'.format(self.regs.rip))
        dbg_info('rax = {:016X}'.format(self.regs.rax))
        dbg_info('rbx = {:016X}'.format(self.regs.rbx))
        dbg_info('rcx = {:016X}'.format(self.regs.rcx))
        dbg_info('rdx = {:016X}'.format(self.regs.rdx))
        dbg_info('rdi = {:016X}'.format(self.regs.rdi))
        dbg_info('rsi = {:016X}'.format(self.regs.rsi))
        dbg_info('r8  = {:016X}'.format(self.regs.r8))
        dbg_info('r9  = {:016X}'.format(self.regs.r9))
        dbg_info('r10 = {:016X}'.format(self.regs.r10))
        dbg_info('r11 = {:016X}'.format(self.regs.r11))
        dbg_info('r12 = {:016X}'.format(self.regs.r12))
        dbg_info('r13 = {:016X}'.format(self.regs.r13))
        dbg_info('r14 = {:016X}'.format(self.regs.r14))
        dbg_info('r15 = {:016X}'.format(self.regs.r15))
        dbg_info('rsp = {:016X}'.format(self.regs.rsp))
        dbg_info('rbp = {:016X}'.format(self.regs.rbp))
        return 
    
    def singlestep_forward(self):
        #singlestep debugging mode
        assert self.libc, "[*]libc instance is None"
        if self.libc.ptrace((PTRACE_SINGLESTEP), self.pid, 0, 0) != 0:
            self.libc.perror("singlestep error: ")
        return 

    def detach(self):
        #detach the debugger from here.
        assert self.libc, "[*]libc instance is None"
        if self.libc.ptrace((PTRACE_DETACH), self.pid, 0, 0) != 0:
            self.libc.perror("detach error: ")
        return 

    #try to match the input string directly, or fail, will search 
    #all mapping segment, try to find the first match.
    def get_mappingof(self, search_key):

        mapping_seg = []
        try:
            mapping_seg = self.mappings[search_key]
        except:
            keys = self.mappings.keys()
            for key in keys:
                if search_key in key:
                    mapping_seg = self.mappings[key]
                    break
        for content in mapping_seg :

            print content

        #print "show target mapping info finished."

#interface
def dbg(pid):

    pid = get_pid(pid)
    mem_mgr = mem(pid)
    p = debugger(pid, mem_mgr.proc_segs)
    return p

