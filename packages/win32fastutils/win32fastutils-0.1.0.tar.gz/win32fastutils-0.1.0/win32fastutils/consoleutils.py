

import encodings
import time
import typing
import multiprocessing
import subprocess

from win32api import MapVirtualKey

import ctypes
from ctypes import Structure
from ctypes import Union
from ctypes import byref
from ctypes import create_unicode_buffer
from ctypes import windll
from ctypes.wintypes import DWORD
from ctypes.wintypes import SHORT
from ctypes.wintypes import BOOL
from ctypes.wintypes import WORD
from ctypes.wintypes import WCHAR
from ctypes.wintypes import CHAR
from ctypes.wintypes import UINT
from ctypes.wintypes import HANDLE

class COORD(Structure):
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT),
    ]

class KEY_EVENT_RECORD_UCHAR_UNION(Union):
    _fields_ = [
        ("UnicodeChar", WCHAR),
        ("AsciiChar", CHAR),
    ]

class KEY_EVENT_RECORD(Structure):
    _fields_ = [
        ("bKeyDown", BOOL),
        ("wRepeatCount", WORD),
        ("wVirtualKeyCode", WORD),
        ("wVirtualScanCode", WORD),
        ("uChar", KEY_EVENT_RECORD_UCHAR_UNION),
        ("dwControlKeyState", DWORD),
    ]

class MOUSE_EVENT_RECORD(Structure):
    _fields_ = [
        ("dwMousePosition", COORD),
        ("dwButtonState", DWORD),
        ("dwControlKeyState", DWORD),
        ("dwControlKeyState", DWORD),
        ("dwEventFlags", DWORD),
    ]

class WINDOW_BUFFER_SIZE_RECORD(Structure):
    _fields_ = [
        ("dwSize", COORD),
    ]

class MENU_EVENT_RECORD(Structure):
    _fields_ = [
        ("dwCommandId", UINT),
    ]

class FOCUS_EVENT_RECORD(Structure):
    _fields_ = [
        ("bSetFocus", BOOL),
    ]

class INPUT_RECORD_EVENT_UNION(Union):
    _fields_ = [
        ("KeyEvent", KEY_EVENT_RECORD),
        ("MouseEvent", MOUSE_EVENT_RECORD),
        ("WindowBufferSizeEvent", WINDOW_BUFFER_SIZE_RECORD),
        ("MenuEvent", MENU_EVENT_RECORD),
        ("FocusEvent", FOCUS_EVENT_RECORD),
    ]

class INPUT_RECORD(Structure):
    _fields_ = [
        ("EventType", WORD),
        ("Event", INPUT_RECORD_EVENT_UNION)
    ]

MAPVK_VK_TO_VSC = 0

FOCUS_EVENT = WORD(0x0010)
KEY_EVENT = WORD(0x0001)
MENU_EVENT = WORD(0x0008)
MOUSE_EVENT = WORD(0x0002)
WINDOW_BUFFER_SIZE_EVENT = WORD(0x0004)

STD_INPUT_HANDLE_CODE = DWORD(-10)
STD_OUTPUT_HANDLE_CODE = DWORD(-11)
STD_ERROR_HANDLE_CODE = DWORD(-12)

STD_INPUT_HANDLE = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE_CODE)
STD_OUTPUT_HANDLE = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE_CODE)
STD_ERROR_HANDLE = windll.kernel32.GetStdHandle(STD_ERROR_HANDLE_CODE)

FreeConsole = windll.kernel32.FreeConsole
AttachConsole = windll.kernel32.AttachConsole
AllocConsole = windll.kernel32.AllocConsole
ReadConsoleOutputCharacterW = windll.kernel32.ReadConsoleOutputCharacterW
ReadConsoleOutputCharacterA = windll.kernel32.ReadConsoleOutputCharacterA
WriteConsoleInputW = windll.kernel32.WriteConsoleInputW
WriteConsoleInputA = windll.kernel32.WriteConsoleInputA


class ResetableAttachConsole(object):
    """Attach to another process' console and re-attach to the original console.
    """

    def __init__(self, processId:int):
        self.processId = processId
        self.consoleHolderEvent = multiprocessing.Event()
    
    def __enter__(self, *args, **kwargs):
        self.attach()

    def __exit__(self, *args, **kwargs):
        self.reset()

    def attach(self, timeout:float=5.0):
        stime = time.time()
        self.consoleHolderProcess = multiprocessing.Process(target=self.currentConsoleHolder, daemon=True)
        self.consoleHolderProcess.start()
        FreeConsole()
        AttachConsole(DWORD(self.processId))
        while True: # wait subprocess start
            if self.consoleHolderProcess.is_alive():
                break
            if time.time() - stime > timeout:
                break
            time.sleep(0.01)

    def reset(self):
        FreeConsole()
        AttachConsole(self.consoleHolderProcess.pid)
        self.consoleHolderEvent.set()

    def currentConsoleHolder(self):
        self.consoleHolderEvent.wait()

def ReadConsoleOutputText(buffer_size:int=1024*1024, handler:HANDLE=STD_OUTPUT_HANDLE, processId:int=None) -> str:
    """Get process console's stdout text.
    """
    def _main():
        outBuffer = create_unicode_buffer(buffer_size)
        outTextLength = DWORD()
        inTopleft = COORD(0, 0)
        ReadConsoleOutputCharacterW(
            handler,
            outBuffer,
            DWORD(buffer_size),
            inTopleft,
            byref(outTextLength),
        )
        return outBuffer.value.strip()

    if processId:
        with ResetableAttachConsole(processId):
            return _main()
    else:
        return _main()
