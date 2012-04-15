#coding: utf-8
import unicodedata
import re

def getTerminalSize():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])

def splitByLength(str, num):
    s = ''
    j = 0
    l = []
    for i in str:
        s += i
        j += 1
        result = re.search(r'[^ -~｡-ﾟ]', i)
        if result:
            j += 1
        if j >= num-1:
            l.append(s)
            j = 0
            s = ''
    if s:
        l.append(s)
    return l
