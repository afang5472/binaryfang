#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from pwn import *

context.log_level = "debug"

p = process("./sshtty.py")

p.recvuntil("password: ")

p.sendline("guest")

print p.recvuntil("turned off")

p.sendline("id")
print p.recvuntil("1000")
p.interactive()
