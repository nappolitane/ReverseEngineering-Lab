# Lab 0x04 (Task 2)

In this task we have a Linux ELF that asks for a password. This lab is about debugging so we will *mainly* use **edb-debugger** to reverse engineer it, and find the correct input.

First we need to open the ELF with IDA and try to find the **ptrace** function and the address from where it is called, so we can bypass the anti-debugging mechanism. We will look inside the *imports* tab and we can find the function there.

![alt text](imports.png?raw=true)

From the *imports tab* we double click on the function and go to the GOT table. Here we find the offset address of where the function will be at runtime. If we right-click on the offset address and use the xref functionality will get to the function that calls the ptrace function and then we can decompile it.

![alt text](ptrace.png?raw=true)

As we can see based on the ptrace result (if the program is being debugged) it will print "Do not debug me" and stop the program. We can get the address after the ptrace call and modify its response inside edb-debugger.

![alt text](modifyrax.png?raw=true)

After we bypass this anti-debugging mechanism we go and look inside the main function of this ELF. We can see that there will be called 2 functions. One is total garbage and the other one is modifying bytes from memory.

![alt text](secondfunc.png?raw=true)

We can see the start address **0x004011C7** and the end address **0x004012CB** that this function is modifying and the way of how it is modifying which is applying bitwise NOT operation. Which (hint) is actually the address of the other function that was garbage. This function acts as a decryption for that function. We have to patch the ELF with the correct decrypted function and look at it with IDA so we can see what it does, and maybe find the correct password. First we set a breakpoint on the address of the instruction after the decryption loop, and dump the memory.

![alt text](decryptedfunc.png?raw=true)

In the above image we can see the "decrypted" memory inside edb and the "encrypted" memory inside GHex editor on task2 ELF, and we can see that those 2 match exactly from the start address and end address we found earlier (if applied bitwise NOT operation). So we can actually modify the ELF and then open it with IDA. We can "patch" the ELF using the following script that changes the bytes from the start to the end address applying NOT operation.

```
#include <stdio.h>

long getfilesize(const char* fname)
{
	FILE* fp;
	fp = fopen(fname, "r");
	fseek(fp, 0, SEEK_END);
	long sz = ftell(fp);
	fclose(fp);
	return sz;
}

int main()
{
	long fsize = getfilesize("task2");

	FILE* fp;
	fp = fopen("task2", "r");
	char fstr[fsize];
	fread(fstr, 1, fsize, fp);
	fclose(fp);
	
	int start = 0x11C7;
	int end = 0x12CB;
	for(int i=start; i<end; i++){
		fstr[i] = ~(fstr[i]);
	}
	
	fp = fopen("patched_task2", "w");
	fwrite(fstr, 1, fsize, fp);
	fclose(fp);

	return 0;
}
```

Now we get the resulted binary, open it with IDA and open the "garbage" function.

![alt text](passwcheck.png?raw=true)

We can see this function is actually the password checking function. Now we can set a breakpoint before it starts checking the user input with the actual password.

![alt text](correctpassw.png?raw=true)

As we can see in the image we can read what is on the **stack** and we find the correct password *dynamic_analysis_is_the_best*

