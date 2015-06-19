import ctypes
 
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
GetClassName = ctypes.windll.user32.GetClassNameW
SwitchToThisWindow = ctypes.windll.user32.SwitchToThisWindow
 
we_are_in_labview = None

def get_title(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def get_cls(hwnd):
    buff = ctypes.create_unicode_buffer(100)
    GetClassName(hwnd, buff, 99)
    return buff.value

def foreach_window(hwnd, lParam):
    global we_are_in_labview

    title, cls = get_title(hwnd), get_cls(hwnd)
    
    if IsWindowVisible(hwnd):
        title, cls = get_title(hwnd), get_cls(hwnd)
        
        if (title, cls) in (('Start', 'Button'), ('', 'Shell_TrayWnd')) or \
           cls == 'TeamViewer_TitleBarButtonClass':
            pass
        else:
            if we_are_in_labview is None:
                we_are_in_labview = cls.startswith('LV')
            else:
                if we_are_in_labview and cls.startswith('LV'):
                    pass
                else:
                    SwitchToThisWindow(hwnd, True)
                    return False
    return True

EnumWindows(EnumWindowsProc(foreach_window), 0)
 
