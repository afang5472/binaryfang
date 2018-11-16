#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports
import os
import sys
import ctypes
 
libc = ctypes.CDLL('libc.so.6')
PTRACE_TRACEME = 0
PTRACE_SINGLESTEP = 9
PTRACE_GETREGS = 12
 
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
 
def wifstopped(status):
    return (status & 0xff) == 0x7f
 
if __name__ == '__main__':
    pid = os.fork() 
    if pid == 0: #zero for child process, {pid} for new process.
        # We are the new child process, this will become the debuggee!
 
        # Allow the process to be ptraced
        libc.ptrace(PTRACE_TRACEME, 0, 0, 0) #please trace me..! the parent will trace u!
 
        # Launch the intended program:
        os.execv(sys.argv[1], sys.argv[1:])
    else:
        _, status = os.wait()
        print(status, hex(status))
        regs = UserRegsStruct()
        while wifstopped(status):
            libc.ptrace(PTRACE_GETREGS, pid, 0, ctypes.byref(regs))
            print('rip = {:016X}'.format(regs.rip))
            print('rax = {:016X}'.format(regs.rax))
            print('rbx = {:016X}'.format(regs.rbx))
            print('rcx = {:016X}'.format(regs.rcx))
            print('rdx = {:016X}'.format(regs.rdx))
            print('rdi = {:016X}'.format(regs.rdi))
            print('rsi = {:016X}'.format(regs.rsi))
            libc.ptrace(PTRACE_SINGLESTEP, pid, 0, 0)
            wait("me")
            _, status = os.wait()
