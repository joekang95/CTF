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

