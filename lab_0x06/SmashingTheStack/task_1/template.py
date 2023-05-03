from pwn import *


io = process("./task1")

io.recvuntil("Enter password:")

io.sendline("let_me_in")

io.interactive()
