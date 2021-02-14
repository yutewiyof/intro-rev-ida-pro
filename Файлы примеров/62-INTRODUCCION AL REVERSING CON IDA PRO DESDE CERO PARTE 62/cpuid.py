# -*- coding: utf-8 -*-
#
#     Copyright (c) 2014 Anders Høst
#

from __future__ import print_function

import platform
import os
import ctypes
from ctypes import c_uint32, c_int, c_long, c_ulong, c_size_t, c_void_p, POINTER, CFUNCTYPE

# Posix x86_64:
# Two first call registers : RDI, RSI
# Volatile registers       : RAX, RCX, RDX, RSI, RDI, R8-11

# Windows x86_64:
# Two first call registers : RCX, RDX
# Volatile registers       : RAX, RCX, RDX, R8-11

# cdecl 32 bit:
# Two first call registers : Stack (%esp)
# Volatile registers       : EAX, ECX, EDX

_POSIX_64_OPC = [
        0x53,                    # push   %rbx
        0x48, 0x89, 0xf0,        # mov    %rsi,%rax
        0x31, 0xc9,              # xor    %ecx,%ecx
        0x0f, 0xa2,              # cpuid
        0x89, 0x07,              # mov    %eax,(%rdi)
        0x89, 0x5f, 0x04,        # mov    %ebx,0x4(%rdi)
        0x89, 0x4f, 0x08,        # mov    %ecx,0x8(%rdi)
        0x89, 0x57, 0x0c,        # mov    %edx,0xc(%rdi)
        0x5b,                    # pop    %rbx
        0xc3                     # retq
]

_WINDOWS_64_OPC = [
        0x53,                    # push   %rbx
        0x48, 0x89, 0xd0,        # mov    %rdx,%rax
        0x49, 0x89, 0xc8,        # mov    %rcx, %r8
        0x31, 0xc9,              # xor    %ecx,%ecx
        0x0f, 0xa2,              # cpuid
        0x41, 0x89, 0x00,        # mov    %eax,(%r8)
        0x41, 0x89, 0x58, 0x04,  # mov    %ebx,0x4(%r8)
        0x41, 0x89, 0x48, 0x08,  # mov    %ecx,0x8(%r8)
        0x41, 0x89, 0x50, 0x0c,  # mov    %edx,0xc(%r8)
        0x5b,                    # pop    %rbx
        0xc3                     # retq
]

_CDECL_32_OPC = [
        0x53,                    # push   %ebx
        0x57,                    # push   %edi
        0x8b, 0x7c, 0x24, 0x0c,  # mov    0xc(%esp),%edi
        0x8b, 0x44, 0x24, 0x10,  # mov    0x10(%esp),%eax
        0x31, 0xc9,              # xor    %ecx,%ecx
        0x0f, 0xa2,              # cpuid
        0x89, 0x07,              # mov    %eax,(%edi)
        0x89, 0x5f, 0x04,        # mov    %ebx,0x4(%edi)
        0x89, 0x4f, 0x08,        # mov    %ecx,0x8(%edi)
        0x89, 0x57, 0x0c,        # mov    %edx,0xc(%edi)
        0x5f,                    # pop    %edi
        0x5b,                    # pop    %ebx
        0xc3                     # ret
]

is_windows = os.name == "nt"
is_64bit   = ctypes.sizeof(ctypes.c_voidp) == 8

class CPUID_struct(ctypes.Structure):
    _fields_ = [(r, c_uint32) for r in ("eax", "ebx", "ecx", "edx")]

class CPUID(object):
    def __init__(self):
        if platform.machine() not in ("AMD64", "x86_64", "x86", "i686"):
            raise SystemError("Only available for x86")
        
        if is_windows:
            if is_64bit:
                # VirtualAlloc seems to fail under some weird
                # circumstances when ctypes.windll.kernel32 is
                # used under 64 bit Python. CDLL fixes this.
                self.win = ctypes.CDLL("kernel32.dll")
                opc = _WINDOWS_64_OPC
            else:
                # Here ctypes.windll.kernel32 is needed to get the
                # right DLL. Otherwise it will fail when running
                # 32 bit Python on 64 bit Windows.
                self.win = ctypes.windll.kernel32
                opc = _CDECL_32_OPC
        else:
            opc = _POSIX_64_OPC if is_64bit else _CDECL_32_OPC

        size = len(opc)
        code = (ctypes.c_ubyte * size)(*opc)

        self.r = CPUID_struct()

        if is_windows:
            self.win.VirtualAlloc.restype = c_void_p
            self.win.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.c_ulong]
            self.addr = self.win.VirtualAlloc(None, size, 0x1000, 0x40)
            if not self.addr:
                raise MemoryError("Could not allocate RWX memory")
        else:
            self.libc = ctypes.cdll.LoadLibrary(None)
            self.libc.valloc.restype = ctypes.c_void_p
            self.libc.valloc.argtypes = [ctypes.c_size_t]
            self.addr = self.libc.valloc(size)
            if not self.addr:
                raise MemoryError("Could not allocate memory")

            self.libc.mprotect.restype = c_int
            self.libc.mprotect.argtypes = [c_void_p, c_size_t, c_int]
            ret = self.libc.mprotect(self.addr, size, 1 | 2 | 4)
            if ret != 0:
                raise OSError("Failed to set RWX")


        ctypes.memmove(self.addr, code, size)

        func_type = CFUNCTYPE(None, POINTER(CPUID_struct), c_uint32)
        self.func_ptr = func_type(self.addr)

    def __call__(self, eax):
        self.func_ptr(self.r, eax)
        return (self.r.eax, self.r.ebx, self.r.ecx, self.r.edx)

    def __del__(self):
        if is_windows:
            self.win.VirtualFree.restype = c_long
            self.win.VirtualFree.argtypes = [c_void_p, c_size_t, c_ulong]
            self.win.VirtualFree(self.addr, 0, 0x8000)
        elif self.libc:
            # Seems to throw exception when the program ends and
            # libc is cleaned up before the object?
            self.libc.free.restype = None
            self.libc.free.argtypes = [c_void_p]
            self.libc.free(self.addr)

if __name__ == "__main__":
    def valid_inputs():
        cpuid = CPUID()
        for eax in (0x0, 0x80000000):
            highest, _, _, _ = cpuid(eax)
            while eax <= highest:
                regs = cpuid(eax)
                yield (eax, regs)
                eax += 1

    print(" ".join(x.ljust(8) for x in ("CPUID", "A", "B", "C", "D")).strip())
    for eax, regs in valid_inputs():
        print("%08x" % eax, " ".join("%08x" % reg for reg in regs))

