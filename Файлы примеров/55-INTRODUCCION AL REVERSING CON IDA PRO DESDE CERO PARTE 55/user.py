import win32api
import win32file
import winioctlcon

FILE_DEVICE_HELLOWORLD=0x00008337
METHOD_BUFFERED = 0
FILE_ANY_ACCESS =0

IOCTL_HOOK =winioctlcon.CTL_CODE( FILE_DEVICE_HELLOWORLD, 0x01, METHOD_BUFFERED, FILE_ANY_ACCESS )
IOCTL_UNHOOK =winioctlcon.CTL_CODE( FILE_DEVICE_HELLOWORLD, 0x02, METHOD_BUFFERED, FILE_ANY_ACCESS )


IOCTL_SAYHELLO=winioctlcon.CTL_CODE( FILE_DEVICE_HELLOWORLD, 0x00, METHOD_BUFFERED, FILE_ANY_ACCESS )
hDevice = win32file.CreateFile(r"\\.\HelloWorld",win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None,win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, 0)

print int(hDevice)

while 1:
    print "1=HELLO\n","2=HOOK\n","3=UNHOOK\n","0=UNHOOK AND EXIT\n"

    case=raw_input()
    if case =="0":
        break
    if case =="1":
        win32file.DeviceIoControl(hDevice,IOCTL_SAYHELLO, None, None, None)
    if case == "2":
        win32file.DeviceIoControl(hDevice,IOCTL_HOOK, None, None, None)
    if case == "3":
        win32file.DeviceIoControl(hDevice,IOCTL_UNHOOK, None, None, None)

win32file.DeviceIoControl(hDevice,IOCTL_UNHOOK, None, None, None)
win32file.CloseHandle(hDevice)
