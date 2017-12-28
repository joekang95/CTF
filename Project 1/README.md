# CTF - PWN

<h2>Content</h2>

* Babay BOF
* Luck
* Shellcode
* Shellcode Revenge
* ROP
* Ret2Libc
* Shellcode Revenge++
* ROP Revenge
* End

<h2>System</h2>
<h3>Linux x86-64</h3>

<h2>Tools</h2>

  * Pwntools (Python3)
  
        sudo apt-get update
        sudo apt-get install python3 python3-dev python3-pip git
        pip3 install --upgrade git+https://github.com/arthaud/python3-pwntools.git
    * https://github.com/arthaud/python3-pwntools

  * gdb-peda
  
        git clone https://github.com/longld/peda.git ~/peda
        echo "source ~/peda/peda.py" >> ~/.gdbinit
      * https://github.com/longld/peda

  * ROPgadget
  
        sudo pip install capstone
        pip install ropgadget
      * https://github.com/JonathanSalwan/ROPgadget
