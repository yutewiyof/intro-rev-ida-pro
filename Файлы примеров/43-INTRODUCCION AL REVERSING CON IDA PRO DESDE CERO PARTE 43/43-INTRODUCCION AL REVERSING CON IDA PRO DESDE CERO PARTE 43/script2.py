from os import *
import struct


stdin,stdout = popen4(r'PRACTICA41b.exe -1')
print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

#rop_chain = create_rop_chain()

fruta="A" * 1000 + "\n"

print stdin


print "Escribe: " + fruta
stdin.write(fruta)
print stdout.read(40)


