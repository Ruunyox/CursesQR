from qrcodegen import QrCode
import numpy as np
import os
import matplotlib.pyplot as plt
import curses

my_code = QrCode.encode_text("Hello World! My name is nick and I am a real live boy", QrCode.Ecc.LOW)
pattern = np.array(my_code._modules).astype('int32') 


class _Canvas():
    """Base class for canvases"""

    def __init__(self, fg=7, bg=9):
        self.fg = fg
        self.bg =bg

    def draw():
        raise NotImplementedError("draw() method must be implemented "
                                  "in child class.")


class stdoutCanvas(_Canvas):
    """Canvas for displaying QR codes straight to stdout"""

    def __init__(self, **kwargs):
        super(stdoutCanvas, self).__init__(**kwargs)

    def draw(self, pattern):
        """draws the QR code pattern on the screen"""
        for module_y in range(len(pattern)):
            for module_x in range(len(pattern)):
                if pattern[module_x][module_y]:
                    print("\033[31;4{}m  ".format(self.fg), end='')
                    print("\033[39;49m", end='')
                else:
                    print("\033[31;4{}m  ".format(self.bg), end='');
                    print("\033[39;49m", end='');
            print("\n", end='')


class UnicodeCanvas(_Canvas):
    """Canvas for displaying QR codes using unicode characters"""

    def __init__(self, char_code, **kwargs):
        super(UnicodeCanvas, self).__init__(**kwargs)
        self.char_code = int(char_code, 16)
        self.string = chr(self.char_code)

    def draw(self, pattern):
        """draws the QR code pattern on the screen"""
        for module_y in range(len(pattern)):
            for module_x in range(len(pattern)):
                if pattern[module_x][module_y]:
                    print(self.string, end='')
                    print(self.string, end='')
                else:
                    print("  ".format(self.bg), end='');
            print("\n", end='')


class CursesCanvas(_Canvas):
    """Canvas for displaying QR codes in a curses window"""

    def __init__(self, screen_bg=4, screen_fg=7, code_bg=4,
                 code_fg=7, text=None, **kwargs):
        super(CursesCanvas, self).__init__(**kwargs)
        self.screen_bg = screen_bg
        self.screen_fg = screen_fg
        self.text = text
        self.curses_init()

    def curses_init(self):
        """Curses initialization routine"""
        self.screen = curses.initscr()
        self.rows, self.cols = self.screen.getmaxyx()
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, self.screen_fg, self.screen_bg)
        curses.init_pair(2, self.fg, self.bg)
        self.screen.keypad(1)
        self.screen.idcok(False)
        self.screen.idlok(False)
        self.screen.bkgd(curses.color_pair(1))
        self.ws_y, self.ws_x = self.screen.getmaxyx()

    def _draw_pattern(self, pattern):
        """Curses routine for drawing the qr code in the window"""
        size = len(pattern)
        self.screen.attron(curses.color_pair(2))
        for module_y in range(size):
            for module_x in range(size):
                if pattern[module_y][module_x]:
                    self.screen.attron(curses.A_REVERSE)
                    self.screen.addstr(module_y + int((self.ws_y - size)/2),
                                       2*module_x + int((self.ws_x - 2*size)/2),
                                       "  ")
                    self.screen.attroff(curses.A_REVERSE)
                else:
                    self.screen.addstr(module_y + int((self.ws_y - size)/2),
                                       2*module_x + int((self.ws_x - 2*size)/2),
                                       "  ")

    def draw(self, pattern):
        """Draws QR code pattern onto curses window"""
        ch = None
        while(ch != ord('q')):
            if self.text:
                self.screen.addstr(1, 1, self.text)
            if 2*pattern.shape[1] > self.screen.getmaxyx()[1]:
                curses.endwin()
                raise RuntimeError("QR code width too large for window width")
            self._draw_pattern(pattern)
            self.screen.refresh()

            ch = self.screen.getch()
            if curses.is_term_resized(self.ws_y, self.ws_x):
                self.screen.clear()
                self.curses_init()
                continue
        curses.endwin()


class QrDisplay():
    """Class for drawing QR codes"""

    def __init__(self, pattern, display_canvas, pad=True):
        self.pattern = pattern
        self.size = pattern.shape[0]
        self.canvas = display_canvas
        if pad:
            # adds 4 null module padding to border of the data feild
            self.pattern = np.vstack((np.zeros((4, self.size)),
                                      self.pattern))
            self.pattern = np.vstack((self.pattern,
                                      np.zeros((4, self.size))))
            self.pattern = np.hstack((np.zeros((self.size+8, 4)),
                                      self.pattern))
            self.pattern = np.hstack((self.pattern,
                                      np.zeros((self.size+8, 4))))
            self.size = self.size + 8

    def draw(self):
        self.canvas.draw(self.pattern)
