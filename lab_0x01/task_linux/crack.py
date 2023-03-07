from pwn import *
from itertools import permutations
import codecs

parts = ["nhnewfhetk","mdcdyamgec","yemlopqosj","hhqtjylumf","jqvanafylz","vlrgmhasbw","zihldazjcn"]
perms = permutations(parts)

for p in perms:
	inp_str = ""
	for word in p:
		inp_str = inp_str + word
	print(inp_str)
	try:
		proc = process(["./crackme"])
		proc.sendline(inp_str)
		hello = proc.recvline()
		hello = proc.recvline()
		hello = proc.recvline()
		print(codecs.decode(hello, 'ascii'))
		print()
		print()
		proc.kill()
	except:
		proc.kill()
		continue

"""
proc = process(["ltrace","./crackme"])
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
proc.sendline("nhnewfhetk"+"mdcdyamgec"+"yemlopqosj"+"hhqtjylumf"+"jqvanafylz"+"vlrgmhasbw"+"zihldazjcn")
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
proc.kill()
"""

"""
for i in range(100):
	try:
		proc = process(["ltrace","./crackme"])
		hello = proc.recvline()
		hello = proc.recvline()
		hello = proc.recvline()
		proc.sendline("a" * i)
		hello = proc.recvline()
		hello = proc.recvline()
		hello = proc.recvline()
		print(hello)
		hello = proc.recvline()
		hello = proc.recvline()
		print(hello)
		print(i)
		hello = proc.recvline()
		print(hello)
	except:
		proc.kill()
		continue
"""
