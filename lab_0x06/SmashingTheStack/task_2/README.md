# Task 2

In this task we have an ELF binary that asks for a password (almost the same as the binary from the first task). We have to buffer overflow it in order to manipulate it as we wish.

The user interaction is the same as in the first task but the correct length now is "8".

In this task we have to overflow the return address of our main function and change it to another function from the binary called *do_login_success*. Below you can see that the main function is kind of the same with the one from the first task.

![alt text](mainfunc.png?raw=true)

Firstly i started debugging the binary in order to visualise the stack and see what is on there.

![alt text](debugger1.png?raw=true)

We can see in the image above the stack with our input (8 "A" chars), and 2 return addresses (as our debugger is telling us). We don't know which one of them we should overflow, and what i did, was to go further with the debugger until the end of the main function and see (at that point in time) what is the first address on the stack because that must be our return address.

![alt text](debugger2.png?raw=true)

As we can see, our return address is the first return address after our input. Now we have to get the address of the *do_login_success* from IDA.

![alt text](loginsuccessfunc.png?raw=true)

As we can see, the address of the start of the function is 0x004011C6. We will write it in reverse because of the little endian. Looking back at the images with the debugger we can see that there are 40 bytes to write and then comes the return address. But we must keep our input to be 8 bytes because of the flow of the main function and bypass that if where it checks the lenght of the password. So our input would be 8 bytes of "A", 32 bytes of "0" and the new return address written in the form of 8 bytes. The python code would look like this:

```
from pwn import *

io = process("./task2")

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
```

![alt text](cracked.png?raw=true)

If we want to exploit a remote service we would change the *process* function with the following:

```
io = process(["/bin/nc", "ip", "port"])
```

