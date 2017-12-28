# ROP

To begin, look at the `rop.c` file:

  ```C
  
  #include<stdio.h>

  int main(){
      setvbuf(stdout,0,2,0);
      puts( "ROP attack is easy, isn't it? Show me your skill." );

      char buf[0x20];
      read( 0  , buf , 200 );

      return 0;
  }
  ```
  
From the title, we know that will we be using Return Oriented Programming (ROP) to solve the problem.

So, what we will need is `ROPgadget` to find out ROP chains for us to use.

When we `objdump -d rop`, we can see that the file is extremley <b>BIG</b>. Thus, we probably do not have to worry about missing or lack of gadgets to use.

Our goal is: <b>`execve("/bin/sh\0", 0, 0)`</b>

A easy way to use is using the `.data section` to store the string "/bin/sh\0". 

  * NOTE: rememeber not to overwrite some imortant data in this section.
  
So let's begin!

First, find the address of `.data section`:

  ```Linux Kernel Module
  objdump -D rop | grep data
  ```
  

