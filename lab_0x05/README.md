# Lab 0x05

In this task we have the Minesweeper game (on 32 bits) from Windows XP and we have to crack it, that means we have to put flags automatically on the bombs so we don't loose the game. Before starting, we get the hint that the game is using the rand function to get the positions of where the bombs will be placed in memory. We get this hint because we will use IDA and as we know IDA does not do any namings, meaning we won't even know where the main function is. So we can find the rand function from imports tab and start from there.

![alt text](retrand.png?raw=true)

We can see in the image above the only function that calls the rand function and as we can see it just returns a random value modulo some number. We will rename it as "ReturnRand" and go inside the only function that calls this function.

![alt text](initmatrix.png?raw=true)

We can't really understand what this function does because of the namings, (although we can see that vector that is using those random values), and it would be very hard and would take a lot of time to go throuh every function. We can just use the x32dbg debugger and see the memory in real time and find what is all about that vector. So we can put a breakpoint at the address where we it does that bitwise OR operation.

![alt text](debugmatrix.png?raw=true)

As we can see in the image above, the debugger gets us to the point where the program loads inside eax a pointer to a memory from data segment which must be our vector, if we follow dump and go to that address we can see in the lower left tab the layout of vector, which looks very much like a matrix, that might be the game matrix layout. Because we can't tell yet for sure anything, we go further with the debugger and see how that bitwise OR operation changes the matrix.

![alt text](debugmatrix2.png?raw=true)

We can see that it does change a byte in our matrix from 0F to 8F value. If we go further, we can see that it changes again another byte from 0F to 8F value, and further again and so on until we have 10 values of 8F inside the matrix. If we think about it, these values might represent where the bombs actually are. Another thing we see is that every 8F value is "between" 2 values of 10. This value might represent the border of one line. So looking back at the image we can see that a bomb might be on the second button. We can click on the first button just to see what happens, inside the game it changes the value to "2" and inside the memory to 42 which is "B", and if we click on the second we see that there was actually a bomb and it changes to CC and all the other bombs to 8A. We can see that in the image below.

![alt text](debugmatrix3.png?raw=true)

So we were right about the bombs. If we do a recap, the matrix has the borders marked with the value 10 and initialises all the values inside with 0F. Using rand function it gets the positions of the bombs changing the values to 8F. Now we can play with it and see what values it gets when we try to put some flags.

![alt text](debugmatrix4.png?raw=true)

Ok so the value for the flag is 0E for a 0F emty button and 8E when there is a bomb. So first thought would be to change those values inside the process memory. But can we do that? Yes, using a Windows API WriteProcessMemory. If the program wouldn't have the matrix inside data segment (meaning a global variable), and it would be dynamically allocated at runtime, it would be much harder to do so. Thinking about this little "crack" and how should i write the code, i realised that all i have to do is to go through entire matrix and change the value in memory from 8F to 8E. We know where is the starting point of the matrix **0x01005340** but the end of it might change it the game would be set to "expert level". So i checked inside the debugger and also with the ReadProcessMemory, to see if i am right about it, the biggest possible matrix of the Minesweeper game.

![alt text](debugmatrix5.png?raw=true)

Looking inside the debugger we can see the address of where the matrix ends that is  **0x01005680**. Using these 2 values we can read the bytes from memory and modify them with 8E when we find a 8F value.

![alt text](cracked.gif?raw=true)

I put the code that i wrote in the repo.

