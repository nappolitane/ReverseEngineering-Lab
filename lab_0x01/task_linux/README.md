# Lab 0x01 (Linux Task)

## The task

We have an obfuscated binary that asks for your input and apply some checks on it. Whenever a check is failed, it will print "WROONG". Use ltrace/strace and python with pwntools library to find the correct input.

We also have a hint. The input is below 100 chars.

## Solution

We run ltrace tool on the binary
```
ltrace ./crackme
```
We type the input and then receive the following:
```
--- SIGSEGV (Segmentation fault) ---
memset(0x8625ae8, '\0', 10000)                                              = 0x8625ae8
--- SIGSEGV (Segmentation fault) ---
fgets(aaaa
"aaaa\n", 10000, 0xf7ef86c0)                                          = 0x8625ae8
--- SIGSEGV (Segmentation fault) ---
strlen("aaaa\n")                                                            = 5
--- SIGSEGV (Segmentation fault) ---
puts("WROOONG!"WROOONG!
)                                                            = 9
--- SIGILL (Illegal instruction) ---
--- SIGSEGV (Segmentation fault) ---
exit(1 <no return ...>
+++ exited (status 1) +++
```
We can see a *strlen* function that must be a check on the input and then the "WRONG" output.
So we have to find the correct length of the input. For that we will use a python script with pwntools.
```
from pwn import *
proc = process(["ltrace","./crackme"])
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
proc.sendline("a" * 10)
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
print(hello)
hello = proc.recvline()
hello = proc.recvline()
print(hello)
proc.kill()
```
We read the output of ltrace line by line and print only the lines we need to see. Running this script we get the following output:
```
[+] Starting local process '/usr/bin/ltrace': pid 12050
crack.py:86: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  proc.sendline("a" * 10)
b'strlen("aaaaaaaaaa\\n")                           = 11\n'
b'puts("WROOONG!"WROOONG!\n'
[*] Stopped process '/usr/bin/ltrace' (pid 12050)
```
Now we got the script that prints out what we need to see, but we have to put it inside a loop and change the length of the input and find the one that is passing the strlen function.
```
from pwn import *
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
```
After running it multiple times, i added the printing of the length of string each round of the loop, and also the next line because it prints out the next check.
```
[+] Starting local process '/usr/bin/ltrace': pid 13712
b'strlen("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"...)    = 70\n'
[*] Process '/usr/bin/ltrace' stopped with exit code 0 (pid 13712)
b'puts("WROOONG!"WROOONG!\n'
69
b')                                 = 9\n'
[+] Starting local process '/usr/bin/ltrace': pid 13715
b'strlen("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"...)    = 71\n'
b'--- SIGSEGV (Segmentation fault) ---\n'
70
b'strstr("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"..., "zihldazjcn") = nil\n'
[+] Starting local process '/usr/bin/ltrace': pid 13718
b'strlen("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"...)    = 72\n'
b'puts("WROOONG!"WROOONG!\n'
71
b')                                 = 9\n'
```
We can see that we got our next check which is the *strstr* fuction. We also got our input length which is 70. But also we get a part of our input string, and we can see that is a 10 chars length string. So we have to find the rest 60 chars.
```
from pwn import *
proc = process(["ltrace","./crackme"])
hello = proc.recvline()
hello = proc.recvline()
hello = proc.recvline()
proc.sendline("zihldazjcn" + "a" * 60)
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
```
After reading and printing lines i got to this second strstr check.
```
[+] Starting local process '/usr/bin/ltrace': pid 14340
crack.py:7: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  proc.sendline("zihldazjcn" + "a" * 60)
b'strlen("zihldazjcnaaaaaaaaaaaaaaaaaaaaaa"...)    = 71\n'
b'strstr("zihldazjcnaaaaaaaaaaaaaaaaaaaaaa"..., "zihldazjcn") = "zihldazjcnaaaaaaaaaaaaaaaaaaaaaa"...\n'
b'strstr("zihldazjcnaaaaaaaaaaaaaaaaaaaaaa"..., "vlrgmhasbw") = nil\n'
[*] Stopped process '/usr/bin/ltrace' (pid 14340)
```
So going forward with reading and printing lines and adding all the other parts to the input string i get to this output
```
[+] Starting local process '/usr/bin/ltrace': pid 16124
crack.py:7: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  proc.sendline("nhnewfhetk"+"mdcdyamgec"+"yemlopqosj"+"hhqtjylumf"+"jqvanafylz"+"vlrgmhasbw"+"zihldazjcn")
b'strlen("nhnewfhetkmdcdyamgecyemlopqosjhh"...)    = 71\n'
b'strstr("nhnewfhetkmdcdyamgecyemlopqosjhh"..., "zihldazjcn") = "zihldazjcn\\n"\n'
b'strstr("nhnewfhetkmdcdyamgecyemlopqosjhh"..., "vlrgmhasbw") = "vlrgmhasbwzihldazjcn\\n"\n'
b'strstr("nhnewfhetkmdcdyamgecyemlopqosjhh"..., "jqvanafylz") = "jqvanafylzvlrgmhasbwzihldazjcn\\n"\n'
b'strstr("nhnewfhetkmdcdyamgecyemlopqosjhh"..., "hhqtjylumf") = "hhqtjylumfjqvanafylzvlrgmhasbwzi"...\n'
b'strstr("nhnewfhetkmdcdyamgecyemlopqosjhh"..., "yemlopqosj") = "yemlopqosjhhqtjylumfjqvanafylzvl"...\n'
b'strstr("nhnewfhetkmdcdyamgecyemlopqosjhh"..., "mdcdyamgec") = "mdcdyamgecyemlopqosjhhqtjylumfjq"...\n'
b'strstr("nhnewfhetkmdcdyamgecyemlopqosjhh"..., "nhnewfhetk") = "nhnewfhetkmdcdyamgecyemlopqosjhh"...\n'
b'puts("Congrats. If that is the correct"...Congrats. If that is the correct input you will now get a flag\n'
b')      = 63\n'
b'puts("If all you see is garbage, try a"...If all you see is garbage, try a different one\n'
b')      = 47\n'
b'strlen("nhnewfhetkmdcdyamgecyemlopqosjhh"...)    = 71\n'
b'strlen("nhnewfhetkmdcdyamgecyemlopqosjhh"...)    = 71\n'
[*] Stopped process '/usr/bin/ltrace' (pid 16124)
```
But when i run again the executable *crackme* using the input string with all the parts i get the garbage output. So before i tested all the permutations of the 7 strings i checked, and found out that the garbage is actually a byte array in hexadecimal format but with some garbage that breaks the byte array. So i will check this string using **codecs.decode(hello,'ascii')** and if it receives an error it will jump to the exception code and it will not print the new lines. So when i will look at the output i will see 2 empty lines in the output, and there it should be the solution.
```
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
```
So the correct input is **nhnewfhetkmdcdyamgeczihldazjcnhhqtjylumfvlrgmhasbwjqvanafylzyemlopqosj** and the flag is **timctf{7dfadd1ee67a9c516c9efbf8f0cf43f4}**

<p align="center">
  <img width="600" height="400" src="https://github.com/nappolitane/ReverseEngineering-Lab/blob/master/lab_0x01/task_linux/ss.png">
</p>

