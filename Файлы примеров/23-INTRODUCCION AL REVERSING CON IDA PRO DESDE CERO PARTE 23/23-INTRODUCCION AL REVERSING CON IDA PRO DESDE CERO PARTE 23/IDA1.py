from subprocess import *
p = Popen([r'C:\Users\ricna\Desktop\New folder (6)\IDA1.exe', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

print "ATACHEA EL DEBUGGER Y APRETA ENTER\n"
raw_input()

primera="A" *140 + "TSRQ\n"
p.stdin.write(primera)

testresult = p.communicate()[0]

print primera
print(testresult)


