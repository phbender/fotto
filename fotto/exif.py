#!/usr/bin/env python

from subprocess import Popen, PIPE
import StringIO

def filehandle(image):
    if isinstance(image, str):
        fh = open(image, 'r')
    else:
        fh = image

    return fh

def imageinfo(image, identify='identify'):

    fh = filehandle(image)

    call = [identify, '-']
    process = Popen(call, stdin=PIPE, stdout=PIPE)
    out, err = process.communicate(fh.read())

    fh.seek(0)

    _fn, _fmt, _size, _, _, _, _, _, _ = out.strip().split()
    _width, _height = map(float, _size.split('x'))

    return dict(
            format=_fmt,
            size = (_width, _height)
            )

def exifdata(image, interesting = None, exiftool='exiftool'):
    """Uses 'exiftool' to access EXIF data. Returns (key, value) pairs.
    Optionally, you can pass a list of interesting keys, if so, only the relevant
    pairs are returned. The 'exiftool' parameter allows to specify a custom
    executable to call. 'image' can be either a file name or a file handle.
    """

    fh = filehandle(image)

    call = [exiftool, '-']

    process = Popen(call, stdin=PIPE, stdout=PIPE)
    out, err = process.communicate(fh.read())

    fh.seek(0)

    res = {}

    lines = [i.split(':') for i in  out.split('\n')]
    for k, v in filter(lambda i: len(i) == 2, lines):
        k = k.strip()
        v = v.strip()

        if interesting is None or k in interesting:
            res[k] = v
    return res

if __name__ == '__main__':

    import sys, itertools
    img_a = open(sys.argv[1])
    img_b = sys.argv[1]

    interest = "Creator Title Description Subject".split()

    t1 = exifdata(img_a, interest)
    t2 = exifdata(img_b, interest)
    for k, v in t1:
        print k, v


