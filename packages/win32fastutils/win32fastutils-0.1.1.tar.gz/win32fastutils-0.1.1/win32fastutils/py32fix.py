from ctypes import windll
from ctypes import byref
from ctypes.wintypes import DWORD
import platform

try:
    Wow64DisableWow64FsRedirection = windll.kernel32.Wow64DisableWow64FsRedirection
    Wow64RevertWow64FsRedirection = windll.kernel32.Wow64RevertWow64FsRedirection
except:
    Wow64DisableWow64FsRedirection = None
    Wow64RevertWow64FsRedirection = None

def iswin32():
    return platform.architecture()[0] == "32bit"

class DisableFileSystemRedirection(object):

    def __init__(self):
        self.oldValue = DWORD()
        self.success = None

    def __enter__(self):
        self.disable()

    def __exit__(self, type, value, traceback):
        self.revert()

    def disable(self):
        if Wow64DisableWow64FsRedirection and iswin32():
            self.success = Wow64DisableWow64FsRedirection(byref(self.oldValue))
        else:
            self.success = None
        return self

    def revert(self):
        if self.success:
            if Wow64RevertWow64FsRedirection:
                Wow64RevertWow64FsRedirection(self.oldValue)
            self.success = None
            self.oldValue = DWORD()

