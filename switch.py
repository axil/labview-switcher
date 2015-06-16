import ctypes
 
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
GetClassName = ctypes.windll.user32.GetClassNameW
SwitchToThisWindow = ctypes.windll.user32.SwitchToThisWindow
 
we_are_in_labview = None
already_switched = False

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
    global we_are_in_labview, already_switched

    title, cls = get_title(hwnd), get_cls(hwnd)
    
    if IsWindowVisible(hwnd):
        title, cls = get_title(hwnd), get_cls(hwnd)
        
        if already_switched:
            return True

        if (title, cls) in (('Start', 'Button'), ('', 'Shell_TrayWnd')):
            return True

        if cls == 'TeamViewer_TitleBarButtonClass':
            return True

        if we_are_in_labview is None:
            we_are_in_labview = cls.startswith('LV')
        else:
            if we_are_in_labview and cls.startswith('LV'):
                return True

            SwitchToThisWindow(hwnd, True)
            already_switched = True
            return True
    return True

EnumWindows(EnumWindowsProc(foreach_window), 0)
 
