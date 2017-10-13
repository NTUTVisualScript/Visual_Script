from tkinter import *
import threading
from ScreenshotUI import ScreenshotUI
from TreeController import Tree

class DumpButton:
    def __init__(self, master):
        self.dumpUI = Button(master, command=lambda: threading.Thread(target=self.dump).start(),
                             text="Capture Screenshot", width=18)
        self.dumpUI.place(x=0, y=30)
        self.tree = Tree.getTree()

    def dump(self):
        threading.Thread(target=ScreenshotUI.getScreenshotUI().getScreenshot).start()
        threading.Thread(target=self.tree.reload).start()
