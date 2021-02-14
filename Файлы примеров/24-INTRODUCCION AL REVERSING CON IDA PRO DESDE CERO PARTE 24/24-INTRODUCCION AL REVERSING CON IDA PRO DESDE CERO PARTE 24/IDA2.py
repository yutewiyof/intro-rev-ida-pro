from subprocess import *
import struct
p = Popen([r'C:\Users\ricna\Desktop\23-INTRODUCCION AL REVERSING CON IDA PRO DESDE CERO PARTE 23\IDA2.exe', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

cookie=struct.pack("<L",0x71727374)
cookie2=struct.pack("<L",0x91929394)
flag=struct.pack("<L",0x90909090)

print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

primera=68 *"A"+ cookie + flag + cookie2
p.stdin.write(primera)

testresult = p.communicate()[0]

print primera
print(testresult)


