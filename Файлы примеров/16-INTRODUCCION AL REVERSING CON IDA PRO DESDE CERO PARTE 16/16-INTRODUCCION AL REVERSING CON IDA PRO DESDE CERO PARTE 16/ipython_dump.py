import idaapi
import idc
import struct

bin=""

file=open("aspack.bin", "wb")

for ea in range (0x400000,0x46e000,4):
    bin+=struct.pack("<L",idc.Dword(ea))

    
file.write(bin)
file.close()