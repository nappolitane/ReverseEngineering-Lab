# Task 1

In this task we have an ELF binary that asks for a password. We have to buffer overflow it in order to manipulate it as we wish.

Initially, i executed the binary to see how it interacts with the user input.

![alt text](usage.png?raw=true)

We can see in the image above that if we give any input that does not have 9 chars it will print "The correct password has length 9", and if we give an input with length 9 it will print "Password mismatch".

Our first subtask would be to make it print "12345" instead of "9" using buffer overflow. In order to do that we will first look inside IDA to see the functions.

![alt text](mainfunc.png?raw=true)

We can see the "if" branch where it prints out "The correct password has length %d" and the variable printed out is "v13".  So we need to overflow this variable on the stack. We can use edb-debugger to debug the binary and visualise the stack and this variable. We will set a breakpoint to the address "0x0040128F" which is the address where the "v13" is set with the value returned from "read" function that we can see in the function inside IDA.

![alt text](passlen.png?raw=true)

We can see in the image above the stack and the value "9" highlighted inside a red square. We go further with the debugger and reach out to the point where we give an input. We will give 10 "A" characters and watch the stack again.

![alt text](buffoverflow.png?raw=true)

We can see our input on the stack. So we can count how many chars we need to input in order to reach that "9" value. A line from the stack has 8 bytes, there are 5 lines and a half, so it would be 44 chars. After that we need to insert the hexa value of "12345" which is "0x3039" but we will insert it in reverse because of little endian. So our python code would look like this:

```
from pwn import *

io = process("./task1")

io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()

io.sendline(b'\x41' * 44 + b'\x39\x30\x00\x00')

hello = io.recvline()
print(hello)
hello = io.recvline()
print(hello)
```

![alt text](correctlen.png?raw=true)

Our second subtask would be to bypass the "memcmp" function by forcing its third parameter to be zero. If we look again at our function from IDA, we can see that we have to do 2 things: first bypass the first if where it checks if the lengths are the same and second is to again overflow to that "v13" variable and set it to "0". Okay so if we know that "v13" must be zero then our "v3" variable (which is the length of the input) must be zero too. So when we overflow we will keep the stack as if we would not put anything there, meaning we put zeros on the stack and overflow to the "v13" and also put zeros. Our python code would remain the same with the following *sendline* function change:

```
io.sendline(b'\x00' * 44 + b'\x00\x00\x00\x00')
```

![alt text](loggedin.png?raw=true)

If we want to exploit a remote service we would change the *process* function with the following:

```
io = process(["/bin/nc", "ip", "port"])
```

