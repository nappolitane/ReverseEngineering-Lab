# Lab 0x02

## Task 1

Using the **Compiler Explorer Godbolt** write short sequences of code and check the resulted assembly code.

1. Write a C function that subtracts two integers. Observe the calling convention (RDI/RSI) and the return value (RAX).

We can observe that the first argument is saved in RDI register and the second argument is saved in the RSI register. Then the return value would be in the RAX register.

2. Write a C function that adds two integers. What assembly instruction did the compiler use?

The compiler used the LEA instruction instead of ADD.

3. Write a C function that adds three integers. What assembly instructions do we have now?

It still uses one LEA instruction but also an ADD instruction before it that adds the first two arguments.

4. Write a C function that adds the first n positive integers. Observe the loop. Try clang compiler. Try optimisation flags O1 and O3. At the beginning of the function fix the number n to a constant value.

Very interesting loop.. When changed to O3 optimisation too many assembly instructions for a sum of integers.. When changed to clang compiler it implemented the n(n+1)/2 formula (pretty impressive) using the shift right instruction. When changed to the constant n value the compiler just precalculated the sum.. WTF?

5. Write a C function that adds the elements in a vector of integers. Try using flags O1 and O3.

When it is used the O1 optimisation, the compiler did the normal thing and put the vector elements on stack and then created a loop where it goes through the stack and adds those vector elements. When used the O3 optimisation the sum was precalculated by the compiler..

6. Define a struct like shown. Access its members using printf. Observe the pointer arithmetic.

The only thing i did observe is that depending on the data type of the member it would create a BYTE, WORD, DWORD, QWORD pointer and before that it will create space on the stack that is always 16 bytes (for two members) not depending on the data type of the members.

7. Analyze the following traversal of a linked list.

The non-optimised version uses the stack to store the values of the current pointer while traversing the list. Whereas the optimised version does not save anything on the stack just goes through the list and test for 0 value.

8. Write a C function that divides an integer by constants 4, 5, 32. Do the same for multiplication by the same constants.

For division the compiler just shifts right in the case of 4 and 32 whereas in the case of 5 it uses a trick to literal division. This trick is based on: multiply the number with the inverse of 5 modulo 2^128, and then it shifts right with the biggest lower than 5 power of 2 that is actually 2. For multiplying is an easy job.

9. Check out the password checking code.

The assembly code is pretty straight forward.

## Task 2

1. Write the C code version for the following assembly.

```
myst2:
	cmp	BYTE PTR [rdi], 0
	je	.L4
	mov eax, 0
.L3:
	add	rax, 1
	cmp	BYTE PTR [rdi+rax], 0
	jne	.L3
	ret
.L4:
	mov	eax, 0
	ret
```
From the "cmp" instructions we can deduce that there is a loop where a pointer variable (which is also the parameter of the function because it is RDI register) is checked on the zero value, and if it is zero the loop will end. From the second "cmp" we also see that the pointer variable with its next double words along it, adding 1 dword every round of the loop. So the code is about an array that is being traversed and checked for a zero value. The return value will be the number of the dwords added until the zero value is reached.
The C code version would be
```
#include <stdint.h>
uint64_t getlength(char* s){
    uint64_t i=0;
    while(s[i]!=0){ i++; }
    return i;
}
```

2. Write the C code version for the following assembly.

```
myst4:
	push	rbp
	push	rbx
	sub	rsp, 8
	mov	rbx, rdi
	cmp	rdi, 1
	ja	.L4
.L2:
	mov	rax, rbx
	add	rsp, 8
	pop	rbx
	pop	rbp
	ret
.L4:
	lea	rdi, [rdi-1]
	call	myst4
	mov	rbp, rax
	lea	rdi, [rbx-2]
	call	myst4
	lea	rbx, [rbp+0+rax]
	jmp	.L2
```
The "cmp" instruction just checks the parameter of the function with value 1 and if it is bigger it will make a self call (which induce the idea of recursion) and with the parameter being the same value but -1, and down the code we can see the same thing but -2, and after that we see that the results saved in "rbp" and "rax" are added and this value returned. IT IS CLEAR we are talking about a fibbonaci function. 
The C code version would be
```
#include <stdint.h>
uint64_t fib(uint64_t n)
{
	if (n > 1) return fib(n - 1) + fib(n - 2);
	return n;
}
```

3. Write the C code version for the following assembly.

```
myst5:
	xor	eax, eax
	cmp	rdi, 1
	jbe	.L1
	cmp	rdi, 3
	jbe	.L6
	test	dil, 1
	je	.L1
	mov	ecx, 2
	jmp	.L3
.L4:
	mov	rax, rdi
	xor	edx, edx
	div	rcx
	test	rdx, rdx
	je	.L8
.L3:
	add	rcx, 1
	mov	rax, rcx
	imul	rax, rcx
	cmp	rax, rdi
	jbe	.L4
.L6:
	mov	eax, 1
	ret
.L8:
	xor	eax, eax
.L1:
	ret
```
First we can see the "cmp" instructions where it checks if the parameter is below 1 where the code returns 0 and then below 3 where it returns 1. Then we can see that at L3 is a loop starting from 2 and the verification is if the counter is below the parameter. If we go to L4 we can see it checks if the parameter divided with the counter is zero that meaning checking for divisors. We can deduce it is about checking if the parameter is a prime number or not, returning 1 if is not and 0 if it is a prime number.
The c code version would be
```
#include <stdint.h>
uint64_t myst5(uint64_t n){
    if(n <= 1) return 0;
    if(n <= 3) return 1;
    for(uint64_t i = 2; i<n; i++){
        if(i*i >= n || n%i == 0) return 1;
    }
    return 0;
}
```

## Task 3

Find out and explain what the following code is doing
```
my_function:
	movabs	rdx, -1085102592571150095
	mov		rax, rdi
	mul		rdx
	mov		rax, rdx
	shr		rax, 4
	ret
```
After seeing the optimised version of a division with 5, i can deduce it is the same thing but another value. In order to calculate the value we have to understand the code. So if we look at the code it multiplies that strange value with the parameter of the function that is about to be divided. I went back to the division with 5 and if we calculate that other value multiplied with the given parameter 5 so the division can be 1, the multiply of that other value with 5 results in the value of 1. This way i figured out that the strange value is actually the inverse of the parameter modulo 2pwr128. So if we calculate the inverse of that strange value we will actually get the number that is 17. Going back to understanding the code, this way of calculating the inverse and then multiplying and then shifting right is just a math trick to avoid direct division.
This code would translate to C like this
```
#include <stdint.h>
uint64_t my_function(uint64_t v){
	return v/17;
}
```

## Task 4

Take the last piece of code presented in Section 2, compile the C program with gcc. Edit the binary file (not the source code!) to make it print "Correct!" when the wrong secret value is given and vice-versa.
```
#include <stdio.h>
#include <stdint.h>
// correct user input is : 0xCD9A0A20 = 3449424416 = 0x1337cafe xor 0xdeadc0de
int main()
{
	uint64_t secret_value = 0xdeadc0de;
	uint64_t user_input;
	scanf("%lld", &user_input);
	user_input ^= 0x1337cafe;
	if (user_input == secret_value) puts("Correct!");
	else puts("Wrong");
	return 0;
}
```
First i tried to use a hex editor and overwrite the "Correct" with "Wrong" and vice-versa but then i realised this CAN work but would not get the same wanted outputs because "Correct" is longer than "Wrong" and we would only print a part of the word so the task wouldn't be correctly done.
Then i looked in the objdump output.
![alt text](objdump.png?raw=true)

So if we look at the code in main we deduce that the "cmp" instruction would be the "if" instruction, and we can see that if it is not equal it will go to 0x11eb and it will call "puts" with the parameter that is calculated with RIP and gives out 0x2012 where we deduce it should be "Wrong" and vice-versa if it is equal it will call "puts" with the parameter calculated with RIP and gives out 0x2009 where it should be "Correct!". I thought that i can rewrite those LEA instructions and calculate RIP with other values, specifically to result in interchanged addresses. So the first to result in 0x2009 and the other to result in 0x2012. So i wrote a script in C "changemain.c" to rewrite the binary with the new LEA instructions. Basically if we look at the LEA instructions we can see the adding operands inside the machine code in little endian (+0xe25 --> .. 3d **25 0e** 00 ..) and (+0xe20 --> .. 3d **20 0e** 00 ..). So when we overwrite the binary we will change these values to the ones that when added to RIP will return in the interchanged values of the adresses of the strings.
![alt text](evidence.png?raw=true)

