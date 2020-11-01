from cursesqr.tools import (stdoutCanvas, UnicodeCanvas, CursesCanvas,
                            QrDisplay)
from qrcodegen import QrCode
import numpy as np
import sys
import argparse

def __main__():

    args = sys.argv[1:]
    opts = argparser(args)

    err_corr = {"LOW": QrCode.Ecc.LOW,
                "MEDIUM": QrCode.Ecc.MEDIUM,
                "QUARTILE": QrCode.Ecc.QUARTILE,
                "HIGH": QrCode.Ecc.HIGH}

    code = QrCode.encode_text(opts.text, err_corr[opts.errlvl])
    pattern = np.array(code._modules).astype('int32')

    if opts.display == "stdout":
        canvas = stdoutCanvas(fg=opts.codefg, bg=opts.codebg)
        qr_out = QrDisplay(pattern, canvas)
        qr_out.draw()
    elif opts.display == "unicode":
        canvas = UnicodeCanvas(opts.char, fg=opts.codefg, bg=opts.codebg)
        qr_out = QrDisplay(pattern, canvas)
        qr_out.draw()
    elif opts.display == "curses":
        canvas = CursesCanvas(screen_fg=opts.screenfg, screen_bg=opts.screenbg,
                              fg=opts.codefg, bg=opts.codebg,
                              text=opts.cursestext)
        qr_out = QrDisplay(pattern, canvas)
        qr_out.draw()
    else:
        raise RuntimeError('display type must be stdout, unicode, or curses.')

def argparser(args):
    parser = argparse.ArgumentParser(description='QR code generator/printer with '
                             'stdout and ncurses display options',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("text", help='text for QR encoding')
    parser.add_argument("--errlvl", help='QR code error level',
                        default="LOW", type=str)
    parser.add_argument("--display", help='QR code display type',
                        default="stdout", type=str)
    parser.add_argument("--codefg", help='QR code foreground color',
                        default=0, type=int)
    parser.add_argument("--codebg", help='QR code background color',
                        default=7, type=int)
    parser.add_argument("--screenfg", help='curses screen foreground color',
                        default=7, type=int)
    parser.add_argument("--screenbg", help='curses screen background color',
                        default=0, type=int)
    parser.add_argument("--cursestext", help='curses screen text',
                        default=None, type=str)
    parser.add_argument("--char", help='unicode character hex number',
                        default='2588', type=str)

    return parser.parse_args(args)


if __name__ == 'cursesqr':
    __main__()
