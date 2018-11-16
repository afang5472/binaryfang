#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports
is_debug = 1

def get_pid(pid_str):

    pid = str(pid_str)
    pid = pid.strip("[").strip("]")
    return pid

def dbg_info(text):

    global is_debug
    if is_debug:
        print text
    else:
        return
