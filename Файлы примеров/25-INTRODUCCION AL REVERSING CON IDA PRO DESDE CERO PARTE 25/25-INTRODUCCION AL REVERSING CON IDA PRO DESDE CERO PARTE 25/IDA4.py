from subprocess import *
import struct
p = Popen([r'C:\Users\ricnar\Desktop\24-INTRODUCCION AL REVERSING CON IDA PRO DESDE CERO PARTE 24\IDA4.exe', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

cookie2="SUrq"
cookie=struct.pack("<L",0x41424344)
flag=struct.pack("<L",0x35224158)
fruta=struct.pack("<L",0x90909090)

print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

primera= 50 *"A"+ cookie2 + cookie + fruta +  flag

p.stdin.write(primera)

testresult = p.communicate()[0]

print primera
print(testresult)


