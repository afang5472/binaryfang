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

PTRACE_TRACEME= 0
PTRACE_ATTACH = 0x10 
PTRACE_GETREGS= 0xc

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

    def _init(self):
        
        #Currently attach a target to be debugged.
        #show parameters right.
        dbg_info("dbg: " + str(self.mappings))
        #load libc && initiate user-regs.
        regs = UserRegsStruct()
	libc = ctypes.CDLL("libc.so.6")
        #attach..!
        ptrace_temp = libc.ptrace((PTRACE_ATTACH), self.pid, 0, 0)
        if ptrace_temp != 0:
            libc.perror("print myfault: ")

        #attacher entering region
        while 1: 
            #wait
            _, status = os.wait()
            #acquire remote control repeatedly.
            libc.ptrace((PTRACE_GETREGS), self.pid, 0, ctypes.byref(regs))
            print('rip = {:016X}'.format(regs.rip))
            print('rax = {:016X}'.format(regs.rax))
            print('rbx = {:016X}'.format(regs.rbx))
            print('rcx = {:016X}'.format(regs.rcx))
            print('rdx = {:016X}'.format(regs.rdx))
            print('rdi = {:016X}'.format(regs.rdi))
            print('rsi = {:016X}'.format(regs.rsi))
	    break
        

#interface
def dbg(pid):

    pid = get_pid(pid)
    mem_mgr = mem(pid)
    p = debugger(pid, mem_mgr.proc_segs)
    return p

