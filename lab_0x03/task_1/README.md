# Lab 0x03 (Task 1)

You have a binary, *riddle*, and also its corresponding source code, *riddle.c*. Using the binary, you will simulate normal reverse engineering by using the source code (instead of guessing). Your task is to create a near-original replica of the original source in the IDA interface.

> **The task:** Rename and retype the 4 functions in the source code (aside the from main). Also rename and retype the stack variables from these 4 functions 

The unedited decompiled version of the main function looks like this
![alt text](f_main.png?raw=true)

If we look at the decompiled source code we can see that the names of the functions and the variables are not the same as in the source code, because the gcc compiler does not store them in the *symbol table* by default.

Next we have the renamed and retyped functions and variables just like the source code is.

![alt text](main.png?raw=true)

![alt text](setup.png?raw=true)

![alt text](chance.png?raw=true)

![alt text](get_rand_string.png?raw=true)

