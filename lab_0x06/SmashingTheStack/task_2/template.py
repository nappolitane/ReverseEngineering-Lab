from pwn import *


io = process("./task2")


io.recvuntil("Enter password:")

gdb.attach(io)

io.sendline("let_me_in")

io.interactive()
