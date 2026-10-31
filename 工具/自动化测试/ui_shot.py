# -*- coding: utf-8 -*-
"""启动程序并在同一进程生命周期内截图（沙箱/CI 环境下子进程会被回收，故必须同脚本完成）。

用法: python ui_shot.py [hold]
输出: 同目录 shot.bmp（24 位 BMP，可直接用任意看图工具打开）
"""
import ctypes
import ctypes.wintypes as wt
import subprocess
import time
import os
import sys

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)   # 必须：否则 150% 缩放下截到逻辑尺寸、坐标错位
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
EXE = os.path.join(ROOT, "工程", "dist", "车辆年检助手.exe")
TITLE = "车辆年检助手"
OUT = os.path.join(HERE, "shot.bmp")


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wt.DWORD), ("biWidth", wt.LONG), ("biHeight", wt.LONG),
                ("biPlanes", wt.WORD), ("biBitCount", wt.WORD), ("biCompression", wt.DWORD),
                ("biSizeImage", wt.DWORD), ("biXPelsPerMeter", wt.LONG),
                ("biYPelsPerMeter", wt.LONG), ("biClrUsed", wt.DWORD), ("biClrImportant", wt.DWORD)]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wt.DWORD * 3)]


def find_main(timeout=25):
    end = time.time() + timeout
    while time.time() < end:
        res = []

        @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        def cb(h, l):
            b = ctypes.create_unicode_buffer(512)
            u32.GetWindowTextW(h, b, 512)
            if b.value.strip() == TITLE:
                res.append(h)
            return True
        u32.EnumWindows(cb, 0)
        if res:
            return res[0]
        time.sleep(0.5)
    return 0


def grab(hwnd, path):
    u32.SetForegroundWindow(hwnd)
    u32.BringWindowToTop(hwnd)
    time.sleep(0.7)
    rc = wt.RECT()
    u32.GetWindowRect(hwnd, ctypes.byref(rc))
    x, y, w, h = rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top
    if w <= 0 or h <= 0:
        print("BAD RECT", x, y, w, h)
        return False
    hdc = u32.GetDC(0)
    mdc = g32.CreateCompatibleDC(hdc)
    bmp = g32.CreateCompatibleBitmap(hdc, w, h)
    g32.SelectObject(mdc, bmp)
    g32.BitBlt(mdc, 0, 0, w, h, hdc, x, y, 0x00CC0020)
    bi = BITMAPINFO()
    bi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bi.bmiHeader.biWidth = w
    bi.bmiHeader.biHeight = h
    bi.bmiHeader.biPlanes = 1
    bi.bmiHeader.biBitCount = 24
    stride = ((w * 24 + 31) // 32) * 4
    buf = ctypes.create_string_buffer(stride * h)
    g32.GetDIBits(mdc, bmp, 0, h, buf, ctypes.byref(bi), 0)
    fh = bytearray()
    fh += b'BM'
    fh += (54 + len(buf)).to_bytes(4, 'little')
    fh += (0).to_bytes(4, 'little')
    fh += (54).to_bytes(4, 'little')
    fh += (40).to_bytes(4, 'little')
    fh += w.to_bytes(4, 'little', signed=True)
    fh += h.to_bytes(4, 'little', signed=True)
    fh += (1).to_bytes(2, 'little')
    fh += (24).to_bytes(2, 'little')
    fh += (0).to_bytes(4, 'little')
    fh += (len(buf)).to_bytes(4, 'little')
    fh += (2835).to_bytes(4, 'little') * 2
    fh += (0).to_bytes(4, 'little') * 2
    with open(path, 'wb') as f:
        f.write(bytes(fh))
        f.write(buf.raw)
    g32.DeleteObject(bmp)
    g32.DeleteDC(mdc)
    u32.ReleaseDC(0, hdc)
    print("SAVED", path, w, "x", h)
    return True


if __name__ == "__main__":
    if not os.path.exists(EXE):
        print("未找到 exe：请先在 aardio 中发布 工程/default.aproj")
        sys.exit(1)
    p = subprocess.Popen([EXE], cwd=os.path.dirname(EXE))
    h = find_main()
    print("hwnd", h)
    if not h:
        print("未找到主窗口")
        sys.exit(1)
    time.sleep(5)
    grab(h, OUT)
    if len(sys.argv) > 1 and sys.argv[1] == "hold":
        time.sleep(30)
    p.terminate()
