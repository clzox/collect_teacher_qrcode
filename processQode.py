"""
@Auth : chenyw
@Time : 2020-04-29-14:28
@File : processQode.py
"""

from tkinter import *


class MainAppWindow:
    def __init__(self, root):
        root.title('ProceeTeacherQode')
        root.geometry('800x600')
        root.resizable(False, False)

        self.menubar = Menu(root)
        self.menubar.add_command(label='加载', command=self.loadfile)
        root.config(menu=self.menubar)

    def loadfile(self):
        pass


if __name__ == "__main__":
    aroot = Tk()
    app = MainAppWindow(aroot)
    mainloop()
