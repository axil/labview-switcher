import ctypes
 
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
GetClassName = ctypes.windll.user32.GetClassNameW
SwitchToThisWindow = ctypes.windll.user32.SwitchToThisWindow
 
i = j = -1
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
    global i, j, we_are_in_labview, already_switched

    try:
        i += 1
        title, cls = get_title(hwnd), get_cls(hwnd)
        open('d:/1.txt', 'a').write(u'{}: {}____{}\n'.format(str(i), title, cls).encode('utf8'))
        
        if IsWindowVisible(hwnd):
            j += 1
            title, cls = get_title(hwnd), get_cls(hwnd)
            open('d:/2.txt', 'a').write(u'{}: {}____{}\n'.format(str(j), title, cls).encode('utf8'))
            
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

                open('d:/1.txt', 'a').write('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')
                open('d:/2.txt', 'a').write('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')
                open('d:/3.txt', 'a').write(u'{}: {}____{}\n'.format(str(j), title, cls).encode('utf8'))
                SwitchToThisWindow(hwnd, True)
                already_switched = True
                return True
        return True
    except Exception, e:
        from traceback import format_exc
        open('d:/4.txt', 'a').write(format_exc())

open('d:/1.txt', 'w').write('')
open('d:/2.txt', 'w').write('')
open('d:/3.txt', 'w').write('')
EnumWindows(EnumWindowsProc(foreach_window), 0)
 
