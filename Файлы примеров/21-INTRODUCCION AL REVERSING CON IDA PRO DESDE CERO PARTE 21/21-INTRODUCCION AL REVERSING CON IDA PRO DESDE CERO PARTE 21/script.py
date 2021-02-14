from subprocess import *
import time
p = Popen([r'C:\Users\ricna\Desktop\20-INTRODUCCION AL REVERSING CON IDA PRO DESDE CERO PARTE 20\NO_VULNERABLE.exe', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

primera="-1\n"
p.stdin.write(primera)
time.sleep(0.5)

segunda="A" *0x2000 + "\n"
p.stdin.write(segunda)

testresult = p.communicate()[0]
time.sleep(0.5)
print(testresult)
print primera
print segunda
