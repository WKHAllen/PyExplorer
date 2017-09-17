import os
import win32api
from idlelib.TreeWidget import *
from Tkinter import *
from ttk import *

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

from idlelib import TreeWidget
TreeWidget.ICONDIR = resource_path("data")

class TreeFileNode(TreeNode):
    def expand(self, event = None):
        if not self.item._IsExpandable():
            return
        if self.state != "expanded":
            self.state = "expanded"
            self.item.state = "expanded"
            self.update()
            self.view()

    def collapse(self, event=None):
        if self.state != "collapsed":
            self.state = "collapsed"
            self.item.state = "collapsed"
            self.update()

class TreeFileItem(FileTreeItem):
    def __init__(self, path):
        self.path = path
        self.state = "collapsed"

    def IsEditable(self):
        return False
        
    def GetIconName(self):
        if self.IsExpandable():
            if self.state == "expanded":
                return "folderOpen.gif"
            return "folderClosed.gif"
        return "file.gif"

    def GetSubList(self):
        try:
            names = os.listdir(self.path)
        except os.error:
            return []
        names.sort(key = os.path.normcase)
        sublist = []
        for name in names:
            sublist.append(TreeFileItem(os.path.join(self.path, name)))
        return sublist

    def OnDoubleClick(self):
        os.startfile(self.path)

class TreeRoot(TreeItem):
    def __init__(self, name):
        self.name = name

    def GetText(self):
        return self.name

    def IsEditable(self):
        return False

    def IsExpandable(self):
        return True

    def GetIconName(self):
        if self.state == "expanded":
            return "folderOpen.gif"
        return "folderClosed.gif"
    
    def GetSubList(self):
        names = win32api.GetLogicalDriveStrings().replace("\\", "/").split("\000")[:-1]
        sublist = []
        for name in names:
            sublist.append(TreeFileItem(name))
        return sublist

class AutoScrollbar(Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"

class ScrolledFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.canvas = Canvas(root, bg = "white", borderwidth = 0, highlightthickness = 0, takefocus = 1)
        self.frame = Frame(self.canvas)
        self.vsb = AutoScrollbar(root, orient = "vertical", command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.vsb.set)
        self.vsb.grid(row = 0, column = 1, sticky = "NS")
        self.canvas.grid(row = 0, column = 0, sticky = "NSEW")
        self.canvas.create_window((0, 0), window = self.frame, anchor = "nw", tags = "self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("PyExplorer")
        self.root.iconbitmap(resource_path(os.path.join("data", "icon.ico")))
        self.root.state("zoomed")
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_columnconfigure(0, weight = 1)
        self.scrolledFrame = ScrolledFrame(self.root)
        self.scrolledFrame.grid(sticky = "NSEW")
        self.scrolledFrame.canvas.bind_all("<MouseWheel>", lambda event: self.scrolledFrame.canvas.yview_scroll(-event.delta / 120, "units"))
        self.item = TreeRoot("Computer")
        self.node = TreeFileNode(self.scrolledFrame.canvas, None, self.item)
        self.node.expand()
        self.root.mainloop()

if __name__ == "__main__":
    App()
