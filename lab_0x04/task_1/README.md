# Lab 0x04 (Task 1)

In this task we have a Windows PE that asks for a password. This lab is about debugging so we will *mainly* use x64dbg to reverse engineer it, and find the correct input.

First we need to open the PE with IDA and try to find the password checking function and the address from where it is called. Same as we did in lab 0x03 we will look inside .rodata section to find the strings that are shown in the interface when we input the password.

![alt text](rodata.png?raw=true)

As we can see in the image we find inside the section the "Try harder" and "Correct" strings and using the **xref** functionality we will jump to the function where they are used.

![alt text](code.png?raw=true)

This is the code of the function and we can already see the *if* instruction that calls the password checking function that is *strcmp*. Also we observe how the *Str1* (user input) and *Str2* (possibly the correct password) are actually constructed, using a function that must be *sprintf* that loads the string with hexadecimals from a vector that has 16 bytes. Now we will get the address of the *if* instruction and set it as a breakpoint inside x64dbg.

![alt text](debugger.png?raw=true)

We can see in the debuger the call of the *strcmp* function and before that would be the two parameters that will be used by the function, *rdx* and *rcx*. If we look at the function inside IDA we will think that *rdx* must be the first parameter corresponding to user input and *rcx* must be the second parameter corresponding to the "correct password", which is actually not true. If we look at the code inside IDA we can see the vector that is constructing the "correct password" and we can check its hexadecimal values and actually find out that they are corresponding to the *rcx* value. That means the *rdx* string value would correspond to user input.
Another task that is in the lab is to make the program show the "Correct" message box. In order to do that we can look again at the debugger screenshot and see that after the *strcmp* call the program checks whether the *rax* value is zero, and if it is it will show the "Correct" message box. That is what we will do.

![alt text](modifyrax.png?raw=true)

You can see above that before executing the *test* instruction the *rax* is 0x01 so we can modify it to be 0x00 and make the program show "Correct" no matter what the input was.

![alt text](modifyrax2.png?raw=true)

Going back to those string values that are checked inside strcmp function we can check if they have a meaning in natural language, but they don't, because they don't correspond to alphabetical ascii characters. Now if we go back to the IDA decompiled code we can see that after the *sprintf* function the user input suffers a slight change. We can revert it using the same exact code.
```
#include <stdio.h>
#include <string.h>

int main()
{
	const char* data = "99fc288bed7238d16d567aa5b3ccd4f5";
	char Str1[33];
	strcpy_s(Str1, 33, data);

	for (int j = 0; j < 16; ++j) {
		char v3 = Str1[j];
		Str1[j] = Str1[31 - j];
		Str1[31 - j] = v3;
	}

	printf("%s\n", Str1);

	return 0;
}
```
Now we get another string that does not have a meaning. All we know is that it represents exactly 16 bytes. We also know that this can be some sort of an encoding or hashing. We will use cyberchef.io to determine if we were right.

![alt text](cyberchef.png?raw=true)

So we actually were right and this string might be a hash. We now check if when our input is hashed will result that string.

![alt text](cyberchef2.png?raw=true)

It does. The string is actually a MD5 hash. So now we have to also revert the "correct password" using the above code and then try to bruteforce it, because we know MD5 can be cracked and we wil use crackstation.net for that.

![alt text](crackstation.png?raw=true)

It worked and we find out that the correct password might be "fmire". Now we will test this input and it is correct!

![alt text](cracked.png?raw=true)

