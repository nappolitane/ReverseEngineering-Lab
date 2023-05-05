from pwn import *

from ctypes import *
libc = CDLL("libc.so.6")
libc.srand(libc.time(0))

rnd = libc.rand()
print hex(rnd)


io = process("./task3")


io.recvuntil("Enter password:")

io.sendline("let_me_in")

io.interactive()
