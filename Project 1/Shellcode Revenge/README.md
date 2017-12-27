# Shellcode Revenge

First, let's take a look at `shellcode_revenge.c`:

  ```C
  #include<stdio.h>

  char code[6];

  int main(){
      setvbuf(stdout,0,2,0);
      puts( "Give me your shellcode , I will execute it directly , but only 6 bytes :(");
      puts( "Six bytes is enough for excellent hacker :)" );

      int (*yuawn)() = (int(*)())code;

      read( 0 , code , 6 );

      puts("Your shellcode is running... 66666666");
      yuawn();

      return 0;
  }
  ```
We can see that `read( 0 , code , 6 )` completely fills up `code[6]` so it is impossible to use that for overflow and yet it is impossible to insert a shellcode that runs `execve("/bin/sh\0", 0, 0)` in 6 bytes.

So, let's go on to `objdump -d shellcode_revenge`:
  
  ```
  400637:	48 c7 45 f8 59 10 60 	movq   $0x601059,-0x8(%rbp)
  40063e:	00 
  40063f:	ba 06 00 00 00       	mov    $0x6,%edx
  400644:	be 59 10 60 00       	mov    $0x601059,%esi
  400649:	bf 00 00 00 00       	mov    $0x0,%edi
  40064e:	b8 00 00 00 00       	mov    $0x0,%eax
  400653:	e8 78 fe ff ff       	callq  4004d0 <read@plt>
  ```
  
We can see that  `read( 0 , code , 6 )` will read to the address `0x601059`, which is the beginning of `code`.

But, we still don't know what to put for a 6-byte shellcode.

Now, it is time for `gdb-peda` and check what are in the registers at the time `yuawn()`, which is our shellcode, is going to run:

