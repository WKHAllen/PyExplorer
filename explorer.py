import pygame, os, sys, subprocess, win32api
from pywl import *

pygame.init()

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

size = (1000, 800)
screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption("PyExplorer")
pygame.display.set_icon(pygame.image.load(resource_path(os.path.join("data", "icon.png"))))
fontsize = 20
font = pygame.font.SysFont("consolas", fontsize)
buttondist = 2
scrollbarwidth = 20

class Tree:
    def __init__(self, name):
        self.name = name
        self.dirs = []
        self.files = []
        self.button = Button(screen, (buttondist, buttondist), (fontsize - (2 * buttondist), fontsize - (2 * buttondist)), text = "+", font = font, color = (0, 0, 0), inactive = (0, 255, 0), active = (63, 255, 63), activated = (127, 255, 127))
        self.text = Textlimit(screen, (fontsize, 0), size[0] - fontsize - scrollbarwidth, name, font = font, color = (0, 0, 0), textpos = "northwest")

    def display(self, ydisplace):
        self.button.pos = (self.button.pos[0], ydisplace + buttondist)
        self.text.pos = (self.text.pos[0], ydisplace + buttondist)
        self.button.display()
        self.text.display()
        newdisplace = ydisplace
        for d in self.dirs:
            newdisplace = d.display(newdisplace + fontsize)
        for f in self.files:
            newdisplace = f.display(newdisplace + fontsize)

    def size(self):
        s = 1
        for d in self.dirs:
            s += d.size()
        for f in self.files:
            s += 1
        return s

    def updateText(self):
        self.text.size = size[0] - fontsize - scrollbarwidth
        for d in self.dirs:
            d.updateText()
        for f in self.files:
            f.text.size = size[0] - (fontsize * 2) - scrollbarwidth

class Dir:
    def __init__(self, path, depth):
        self.path = path
        self.depth = depth
        self.dirs = []
        self.files = []
        self.button = Button(screen, (fontsize * depth + buttondist, buttondist), (fontsize - (2 * buttondist), fontsize - (2 * buttondist)), text = "+", font = font, color = (0, 0, 0), inactive = (0, 255, 0), active = (63, 255, 63), activated = (127, 255, 127))
        if path.count("/") == 1:
            self.text = Textlimit(screen, (fontsize * (depth + 1), 0), size[0] - (fontsize * (depth + 1)) - scrollbarwidth, path[:-1], font = font, color = (0, 0, 0), textpos = "northwest")
        else:
            self.text = Textlimit(screen, (fontsize * (depth + 1), 0), size[0] - (fontsize * (depth + 1)) - scrollbarwidth, os.path.split(path[:-1])[1], font = font, color = (0, 0, 0), textpos = "northwest")

    def display(self, ydisplace):
        self.button.pos = (self.button.pos[0], ydisplace + buttondist)
        self.text.pos = (self.text.pos[0], ydisplace)
        self.button.display()
        self.text.display()
        if self.button.value:
            if self.button.text == "+":
                self.unlock()
            elif self.button.text == "-":
                self.lock()
        newdisplace = ydisplace
        for d in self.dirs:
            newdisplace = d.display(newdisplace + fontsize)
        for f in self.files:
            newdisplace = f.display(newdisplace + fontsize)
        return newdisplace

    def unlock(self):
        self.dirs = []
        self.files = []
        try:
            for d in os.listdir(self.path):
                if os.path.isdir(self.path + d):
                    self.dirs.append(Dir(self.path + d + "/", self.depth + 1))
                elif os.path.isfile(self.path + d):
                    self.files.append(File(self.path + d, self.depth + 1))
        except:
            self.files = [Error(self.depth + 1)]
        self.button = Button(screen, (fontsize * self.depth + buttondist, buttondist), (fontsize - (2 * buttondist), fontsize - (2 * buttondist)), text = "-", font = font, color = (0, 0, 0), inactive = (255, 0, 0), active = (255, 63, 63), activated = (255, 127, 127))

    def lock(self):
        for d in self.dirs:
            d.lock()
        self.dirs = []
        self.files = []
        self.button = Button(screen, (fontsize * self.depth + buttondist, buttondist), (fontsize - (2 * buttondist), fontsize - (2 * buttondist)), text = "+", font = font, color = (0, 0, 0), inactive = (0, 255, 0), active = (63, 255, 63), activated = (127, 255, 127))

    def size(self):
        s = 1
        for d in self.dirs:
            s += d.size()
        for f in self.files:
            s += 1
        return s

    def updateText(self):
        self.text.size = size[0] - (fontsize * (self.depth + 1)) - scrollbarwidth
        for d in self.dirs:
            d.updateText()
        for f in self.files:
            f.text.size = size[0] - (fontsize * (self.depth + 2)) - scrollbarwidth

class File:
    def __init__(self, path, depth):
        self.path = path
        self.depth = depth
        self.button = Button(screen, (fontsize * depth + buttondist, buttondist), (fontsize - (2 * buttondist), fontsize - (2 * buttondist)), text = " ", font = font, color = (0, 0, 0), inactive = (0, 0, 255), active = (63, 63, 255), activated = (127, 127, 255))
        self.text = Textlimit(screen, (fontsize * (depth + 1), 0), size[0] - (fontsize * (depth + 1)) - scrollbarwidth, os.path.split(path)[1], font = font, color = (0, 0, 0), textpos = "northwest")

    def display(self, ydisplace):
        self.button.pos = (self.button.pos[0], ydisplace + buttondist)
        self.text.pos = (self.text.pos[0], ydisplace)
        self.button.display()
        self.text.display()
        if self.button.value:
            subprocess.call("start " + self.path.replace("/", "\\"), shell = True)
        return ydisplace

class Error:
    def __init__(self, depth):
        self.text = Textlimit(screen, (fontsize * (depth + 1), 0), size[0] - (fontsize * (depth + 1)) - scrollbarwidth, "ERROR", font = font, color = (255, 0, 0), textpos = "northwest")

    def display(self, ydisplace):
        self.text.pos = (self.text.pos[0], ydisplace)
        self.text.display()
        return ydisplace

def main():
    global screen, size
    
    root = Tree("Computer")

    scrollbar = Scrollbar(screen, (size[0] - scrollbarwidth, 0), (scrollbarwidth, size[1]), fontsize)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict["size"], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                size = screen.get_size()
                scrollbar.pos = (size[0] - scrollbarwidth, 0)
                scrollbar.size = (scrollbarwidth, size[1])
                root.updateText()

            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scrollbar.value -= 80
                    if scrollbar.value < 0:
                        scrollbar.value = 0
                elif event.button == 5:
                    scrollbar.value += 80
                    if scrollbar.value > scrollbar.scrollsize - size[1] - 1:
                        scrollbar.value = scrollbar.scrollsize - size[1] - 1
                    if scrollbar.value < 0:
                        scrollbar.value = 0

        if scrollbar.value + size[1] >= fontsize * (root.size() + 1):
            if size[1] >= fontsize * (root.size() + 1):
                scrollbar.value = 0
            else:
                scrollbar.value = fontsize * root.size() - scrollbar.size[1] - 1
        
        if root.button.value:
            if root.button.text == "+":
                root.dirs = [Dir(drive[:-1] + "/", 1) for drive in win32api.GetLogicalDriveStrings().split("\000")[:-1]]
                root.button.text = "-"
                root.button.inactive = (255, 0, 0)
                root.button.active = (255, 63, 63)
                root.button.activated = (255, 127, 127)
            elif root.button.text == "-":
                root.dirs = []
                root.button.text = "+"
                root.button.inactive = (0, 255, 0)
                root.button.active = (63, 255, 63)
                root.button.activated = (127, 255, 127)
        
        screen.fill(white)

        scrollbar.scrollsize = fontsize * root.size()
        scrollbar.display()
        root.display(-scrollbar.value)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
