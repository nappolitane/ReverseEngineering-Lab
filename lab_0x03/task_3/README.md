# Lab 0x03 (Task 3)

In this task, you will learn to use the Structures functionality of IDA. Look at the code in main and the password checking function, analyze the access patterns, and verify that it matches the linked list structure below.

First we implement the linked list structure as given
![alt text](structure.png?raw=true)

After renaming and retyping some of the variables in main and the cast of the buffer returned from malloc with the implemented structure we get the main function looking like this
![alt text](main.png?raw=true)

Here you can see the password_check function after the propagation of the renaming and retyping from main and also some renaming and retyping done inside this function
![alt text](passw_check.png?raw=true)

