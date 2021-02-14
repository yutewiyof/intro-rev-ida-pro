sum=0
user=raw_input()
largo=len(user)
if (largo> 0xb):
    exit()

userMAY=""

for i in range(largo):
    if (ord(user[i])<0x41):
        print "CARACTER INVALIDO"
        exit()
    if (ord(user[i]) >= 0x5a):
        userMAY+= chr(ord(user[i])-0x20)
    else:
        userMAY+= chr(ord(user[i]))

print "USER",userMAY

for i in range(len(userMAY)):
    sum+=ord (userMAY[i])

print "SUMATORIA", hex(sum)

xoreado= sum ^ 0x5678
print "XOREADO", hex(xoreado)

TOTAL= xoreado ^ 0x1234

print "PASSWORD", TOTAL




