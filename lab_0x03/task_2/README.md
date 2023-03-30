# Lab 0x03 (Task 2)

In this task, you will learn to navigate through functions in a statically linked and stripped binary named *task2*. Since the binary has a whopping 783 functions detected, you do not have the time or motivation to go through all of them. As such, you need to approach the problem in a clever and elegant way:

First we run the program once to find any string that may help us. Doing so, we get the "I win" string. Then we go to the rodata segment and search for this string.
![alt text](rodata.png?raw=true)

Now we use the **xref** functionality and determine where the main function is.
![alt text](graph.png?raw=true)

Looking at the graph view we can see the comments saying that the function starts at *sub_401DE7*. So we can rename this function as *main*. We can see that this main function has only one function that is calling and using the return value of this function in order to determine if the input was correct or not, printing "You win" or "I win". So we will rename the function as *password_check* and we will also do some renaming here and there (printf/scanf).
![alt text](main.png?raw=true)

Here you can see the unedited version of the password_check function
![alt text](passw_check_1.png?raw=true)

If we go to the first **word_...** variable we get the following view inside IDA, and we can see some chars here and there
![alt text](passw_check_2.png?raw=true)

If we go to the first address inside this data segment and set the strings to be **unicode** we will get the following view
![alt text](passw_check_3.png?raw=true)

It will also change the pseudocode view and we can see what the correct input is: **69F2a+18d346b/SQ5c65e**
![alt text](passw_check_4.png?raw=true)

