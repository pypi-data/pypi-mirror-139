
import time
import typing
import win32api
import win32con
import win32gui
import win32process
from ctypes.wintypes import HWND

import psutil

EXPLORER_NAME = "explorer.exe"

def PostMessage(hwnd:HWND, message:str, interval:float=0.01):
    """Send keys to GUI.
    """
    for c in message:
        time.sleep(interval)
        win32api.PostMessage(hwnd, win32con.WM_CHAR, ord(c), 0)
    time.sleep(interval)


def GetHwndsByProcessIds(*processIds:typing.List[int], visibleOnly=True) -> HWND:
    """Get All visible windows' handler of the given process.
    """
    def callback(hwnd, hwnds):
        if visibleOnly:
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, foundPid = win32process.GetWindowThreadProcessId(hwnd)
                if foundPid in processIds:
                    hwnds.append(hwnd)
        else:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def GetExplorerHwnds(visibleOnly=True):
    """Get explorer.exe hwnds.
    """
    pids = GetExplorerProcessIds()
    return GetHwndsByProcessIds(*pids, visibleOnly=visibleOnly)

def GetExplorerProcessIds():
    """Get explorer.exe pids.
    """
    pids = []
    for proc in psutil.process_iter():
        if proc.name().lower() == EXPLORER_NAME:
            pids.append(proc.pid)
    return pids
