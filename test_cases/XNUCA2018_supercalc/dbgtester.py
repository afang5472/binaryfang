#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from binaryfang import *

context.log_level = "debug"

p = process("./super_calc")

pid = get_pid(pidof(p))

dbger = dbg(pid)

#standard interactive sequence.
p.recvuntil(">>> ")
p.sendline("a=123")
p.recvuntil(">>> ")
p.sendline("a")
p.recvuntil("123")
p.recvuntil(">>> ")
print "Till the end."
p.close()
