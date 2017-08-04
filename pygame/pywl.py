import pygame, sys, datetime

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

defaultFont = pygame.font.SysFont("consolas", 20)

defaultInactive = (191, 191, 191)
defaultActive = (127, 191, 255)
defaultActivated = (63, 127, 255)

border = 3

class Text:
    def __init__(self, screen, pos, text, font = defaultFont, color = black, textpos = "center"):
        self.screen = screen
        self.pos = pos
        self.text = text
        self.font = font
        self.color = color
        self.textpos = textpos

    def display(self):
        textSurf = self.font.render(self.text, True, self.color)
        textRect = textSurf.get_rect()
        
        if self.textpos == "center":
            textRect.center = self.pos[0], self.pos[1]
        elif self.textpos == "north":
            textRect.midtop = self.pos[0], self.pos[1]
        elif self.textpos == "northeast":
            textRect.topright = self.pos[0], self.pos[1]
        elif self.textpos == "east":
            textRect.midright = self.pos[0], self.pos[1]
        elif self.textpos == "southeast":
            textRect.bottomright = self.pos[0], self.pos[1]
        elif self.textpos == "south":
            textRect.midbottom = self.pos[0], self.pos[1]
        elif self.textpos == "southwest":
            textRect.bottomleft = self.pos[0], self.pos[1]
        elif self.textpos == "west":
            textRect.midleft = self.pos[0], self.pos[1]
        elif self.textpos == "northwest":
            textRect.topleft = self.pos[0], self.pos[1]
        
        self.screen.blit(textSurf, textRect)

class Checkbox:
    def __init__(self, screen, pos, size, default = False, inactive = defaultInactive, active = defaultActive, activated = defaultActivated, clickable = True):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.value = default
        self.inactive = inactive
        self.active = active
        self.activated = activated
        self.clickable = clickable
        self.clicking = False

    def display(self):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        pygame.draw.rect(self.screen, black, (self.pos[0], self.pos[1], self.size, self.size))

        if self.pos[0] <= cur[0] < self.pos[0] + self.size and self.pos[1] <= cur[1] < self.pos[1] + self.size and self.clickable:
            if click:
                pygame.draw.rect(self.screen, self.activated, (self.pos[0] + border, self.pos[1] + border, self.size - (2 * border), self.size - (2 * border)))
            else:
                pygame.draw.rect(self.screen, self.active, (self.pos[0] + border, self.pos[1] + border, self.size - (2 * border), self.size - (2 * border)))
        else:
            pygame.draw.rect(self.screen, self.inactive, (self.pos[0] + border, self.pos[1] + border, self.size - (2 * border), self.size - (2 * border)))

        if self.value:
            pygame.draw.line(self.screen, black, (self.pos[0] + (2 * border), self.pos[1] + self.size / 2), (self.pos[0] + self.size / 2, self.pos[1] + self.size - (2 * border)), border)
            pygame.draw.line(self.screen, black, (self.pos[0] + self.size / 2, self.pos[1] + self.size - (2 * border)), (self.pos[0] + self.size - (2 * border), self.pos[1] + (2 * border)), border)
        
        if self.pos[0] <= cur[0] < self.pos[0] + self.size and self.pos[1] <= cur[1] < self.pos[1] + self.size and self.clickable and self.clicking and not click:
            self.value = not self.value
            self.clicking = False
        
        self.clicking = click

class Button:
    def __init__(self, screen, pos, size, text = "", font = defaultFont, color = black, inactive = defaultInactive, active = defaultActive, activated = defaultActivated, clickable = True):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.text = text
        self.font = font
        self.color = color
        self.inactive = inactive
        self.active = active
        self.activated = activated
        self.clickable = clickable
        self.clicking = False
        self.value = False

    def display(self):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        
        self.value = False
        
        pygame.draw.rect(self.screen, black, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        
        if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] <= cur[1] < self.pos[1] + self.size[1] and self.clickable:
            if click:
                pygame.draw.rect(self.screen, self.activated, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))
            else:
                pygame.draw.rect(self.screen, self.active, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))
        else:
            pygame.draw.rect(self.screen, self.inactive, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))

        Text(self.screen, (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2), self.text, font = self.font, color = self.color).display()

        if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] <= cur[1] < self.pos[1] + self.size[1] and self.clickable and self.clicking and not click:
            self.value = True

        self.clicking = click

class Slider:
    def __init__(self, screen, pos, size, interval, default, inactive = defaultInactive, active = defaultActive, activated = defaultActivated, clickable = True):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.interval = interval
        self.value = default
        self.inactive = inactive
        self.active = active
        self.activated = activated
        self.clickable = clickable
        self.clicking = False
    
    def display(self):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        pygame.draw.line(self.screen, black, (self.pos[0] + self.size / 2, self.pos[1] + self.size), (self.pos[0] + self.interval[1] - self.interval[0] + self.size / 2, self.pos[1] + self.size), border)
        pygame.draw.rect(self.screen, black, (self.pos[0] + self.value - self.interval[0], self.pos[1], self.size, self.size))

        if self.pos[0] + self.value - self.interval[0] <= cur[0] < self.pos[0] + self.value - self.interval[0] + self.size and self.pos[1] <= cur[1] < self.pos[1] + self.size and self.clickable:
            if click:
                pygame.draw.rect(self.screen, self.activated, (self.pos[0] + self.value - self.interval[0] + border, self.pos[1] + border, self.size - (2 * border), self.size - (2 * border)))
                self.clicking = True
            else:
                pygame.draw.rect(self.screen, self.active, (self.pos[0] + self.value - self.interval[0] + border, self.pos[1] + border, self.size - (2 * border), self.size - (2 * border)))
        else:
            pygame.draw.rect(self.screen, self.inactive, (self.pos[0] + self.value - self.interval[0] + border, self.pos[1] + border, self.size - (2 * border), self.size - (2 * border)))

        if self.clicking:
            self.value = cur[0] - self.pos[0] + self.interval[0] - self.size / 2
            if self.value < self.interval[0]:
                self.value = self.interval[0]
            elif self.value >= self.interval[1]:
                self.value = self.interval[1] - 1

        if not click:
            self.clicking = False

class Dropdown:
    def __init__(self, screen, pos, size, options, selected = 0, font = defaultFont, color = black, inactive = defaultInactive, active = defaultActive, activated = defaultActivated, clickable = True):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.options = options
        self.value = selected
        self.font = font
        self.color = color
        self.inactive = inactive
        self.active = active
        self.activated = activated
        self.clickable = clickable
        self.clicking = False
        self.open = False

    def display(self):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        pygame.draw.rect(self.screen, black, (self.pos[0], self.pos[1], self.size[0], self.size[1]))

        if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] <= cur[1] < self.pos[1] + self.size[1] and self.clickable:
            if click:
                pygame.draw.rect(self.screen, self.activated, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))
            else:
                pygame.draw.rect(self.screen, self.active, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))
        else:
            pygame.draw.rect(self.screen, self.inactive, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))

        Text(self.screen, (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2), self.options[self.value], font = self.font, color = self.color).display()

        if self.open:
            total = 1
            
            for i in range(len(self.options)):
                if i != self.value:
                    pygame.draw.rect(self.screen, black, (self.pos[0], self.pos[1] + (self.size[1] - border) * total, self.size[0], self.size[1]))
                    
                    if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] + (self.size[1] - border) * total + border <= cur[1] < self.pos[1] + (self.size[1] - border) * (total + 1) + border and self.clickable:
                        if click:
                            pygame.draw.rect(self.screen, self.activated, (self.pos[0] + border, self.pos[1] + border + (self.size[1] - border) * total, self.size[0] - (2 * border), self.size[1] - (2 * border)))
                        else:
                            pygame.draw.rect(self.screen, self.active, (self.pos[0] + border, self.pos[1] + border + (self.size[1] - border) * total, self.size[0] - (2 * border), self.size[1] - (2 * border)))
                    else:
                        pygame.draw.rect(self.screen, self.inactive, (self.pos[0] + border, self.pos[1] + border + (self.size[1] - border) * total, self.size[0] - (2 * border), self.size[1] - (2 * border)))

                    Text(self.screen, (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2 + (self.size[1] - border) * total), self.options[i], font = self.font, color = self.color).display()

                    if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] + (self.size[1] - border) * total + border <= cur[1] < self.pos[1] + (self.size[1] - border) * (total + 1) + border - 1 and self.clickable and self.clicking and not click:
                        self.value = i
                        self.open = False

                    total += 1

        if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] <= cur[1] < self.pos[1] + self.size[1] - 1 and self.clickable and self.clicking and not click:
            self.open = not self.open
        elif self.clicking and not click:
            self.open = False

        self.clicking = click

class Input:
    def __init__(self, screen, pos, size, default = "", font = defaultFont, color = black, limit = 127, cursor = 1, inactive = defaultInactive, active = defaultActive, activated = defaultActivated, clickable = True):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.value = default
        self.font = font
        self.color = color
        self.limit = limit
        self.cursor = cursor
        self.inactive = inactive
        self.active = active
        self.activated = activated
        self.clickable = clickable
        self.clicking = False
        self.open = False
        self.pressing = []

    def display(self):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        
        keys = pygame.key.get_pressed()
        textpos = self.font.render(self.value, True, self.color).get_rect()

        pygame.draw.rect(self.screen, black, (self.pos[0], self.pos[1], self.size[0], self.size[1]))

        if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] <= cur[1] < self.pos[1] + self.size[1] and self.clickable:
            if click:
                pygame.draw.rect(self.screen, self.activated, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))
            else:
                pygame.draw.rect(self.screen, self.active, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))
        else:
            pygame.draw.rect(self.screen, self.inactive, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))

        if self.open:
            pygame.draw.rect(self.screen, self.activated, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))

            if keys[pygame.K_BACKSPACE] and pygame.K_BACKSPACE not in self.pressing:
                self.value = self.value[:-1]
            elif keys[pygame.K_RETURN]:
                self.open = False
            else:
                for i in range(128):
                    if keys[i] and i not in self.pressing and len(self.value) < self.limit and textpos[2] < self.size[0] - (3 * border) - 30:
                        if not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]:
                            self.value += chr(i)
                        else:
                            shift = [39, 34, 44, 60, 45, 95, 46, 62, 47, 63, 48, 41, 49, 33, 50, 64, 51, 35, 52, 36, 53, 37, 54, 94, 55, 38, 56, 42, 57, 40, 59, 58, 61, 43, 91, 123, 92, 124, 93, 125, 96, 126]
                            for j in range(0, len(shift) - 1, 2):
                                if i == shift[j] and shift[j + 1]:
                                    self.value += chr(shift[j + 1])
                            if 97 <= i <= 122:
                                self.value += chr(i - 32)

        if self.open and datetime.datetime.now().microsecond / 500000:
            if self.cursor:
                Text(self.screen, (self.pos[0] + (3 * border), self.pos[1] + self.size[1] / 2), self.value + "|", font = self.font, color = self.color, textpos = "west").display()
            else:
                Text(self.screen, (self.pos[0] + (3 * border), self.pos[1] + self.size[1] / 2), self.value + "_", font = self.font, color = self.color, textpos = "west").display()
        else:
            Text(self.screen, (self.pos[0] + (3 * border), self.pos[1] + self.size[1] / 2), self.value, font = self.font, color = self.color, textpos = "west").display()

        if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] <= cur[1] < self.pos[1] + self.size[1] and self.clickable and self.clicking and not click:
            self.open = True
        elif self.clicking and not click:
            self.open = False

        self.clicking = click

        self.pressing = []
        for k in range(128):
            if keys[k]:
                self.pressing.append(k)

class Window:
    def __init__(self, screen, pos, size, title = "pywl window", font = defaultFont, color = black, wincolor = defaultActivated, options = [], widgets = [], clickable = True):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.title = title
        self.font = font
        self.color = color
        self.wincolor = wincolor
        self.options = [Button(self.screen, (self.size[0] + (4 * border) - (7 * border * (len(options) - i)), 2 * border), (6 * border, 6 * border), inactive = options[i][0], active = options[i][1], activated = options[i][2]) for i in range(len(options))]
        self.widgets = widgets
        self.clickable = clickable
        self.surface = pygame.Surface(size)
        self.surface.fill(white)
        self.clicking = False
        self.clickpos = (0, 0)
        self.selected = False

    def display(self):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        hovering = False
        for option in self.options:
            if self.pos[0] + option.pos[0] <= cur[0] < self.pos[0] + option.pos[0] + option.size[0] and self.pos[1] + option.pos[1] <= cur[1] < self.pos[1] + option.pos[1] + option.size[1] and option.clickable:
                hovering = True

        if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] + (6 * border) and self.pos[1] <= cur[1] < self.pos[1] + (9 * border) and click and not self.clicking and not hovering and self.clickable:
            self.clickpos = cur[0] - self.pos[0], cur[1] - self.pos[1]
            self.selected = True
        elif not click:
            self.selected = False

        if click and self.selected:
            self.pos = cur[0] - self.clickpos[0], cur[1] - self.clickpos[1]

        pygame.draw.rect(self.screen, black, (self.pos[0], self.pos[1], self.size[0] + (6 * border), self.size[1] + (12 * border)))
        pygame.draw.rect(self.screen, self.wincolor, (self.pos[0] + border, self.pos[1] + border, self.size[0] + (4 * border), self.size[1] + (10 * border)))

        Text(self.screen, (self.pos[0] + (3 * border), self.pos[1] + (5 * border)), self.title, font = self.font, color = self.color, textpos = "west").display()

        for option in self.options:
            option.pos = (option.pos[0] + self.pos[0], option.pos[1] + self.pos[1])
            option.display()
            option.pos = (option.pos[0] - self.pos[0], option.pos[1] - self.pos[1])

        self.screen.blit(self.surface, (self.pos[0] + (3 * border), self.pos[1] + (9 * border)))

        for widget in self.widgets:
            widget.pos = (widget.pos[0] + self.pos[0] + (3 * border), widget.pos[1] + self.pos[1] + (9 * border))
            widget.display()
            widget.pos = (widget.pos[0] - self.pos[0] - (3 * border), widget.pos[1] - self.pos[1] - (9 * border))

        self.clicking = click

class Progress:
    def __init__(self, screen, pos, size, percent, color = defaultInactive):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.percent = percent
        self.color = color

    def display(self):
        pygame.draw.rect(self.screen, black, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        pygame.draw.rect(self.screen, self.color, (self.pos[0] + border, self.pos[1] + border, int(self.percent * (self.size[0] - (2 * border))), self.size[1] - (2 * border)))

class Scrollbar:
    def __init__(self, screen, pos, size, scrollsize, default = 0, inactive = defaultInactive, active = defaultActive, activated = defaultActivated, clickable = True):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.scrollsize = scrollsize
        self.value = default
        self.inactive = inactive
        self.active = active
        self.activated = activated
        self.clickable = clickable
        self.clicking = False

    def display(self):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        pygame.draw.rect(self.screen, black, (self.pos[0], self.pos[1], self.size[0], self.size[1]))

        if self.scrollsize >= self.size[1]:
            if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] + (self.size[1] * self.value / float(self.scrollsize)) <= cur[1] < self.pos[1] + (self.size[1] * self.value / float(self.scrollsize)) + self.size[1] ** 2 / self.scrollsize and self.clickable:
                if click:
                    pygame.draw.rect(self.screen, self.activated, (self.pos[0] + border, self.pos[1] + (self.size[1] * self.value / float(self.scrollsize)) + border, self.size[0] - (2 * border), self.size[1] ** 2 / self.scrollsize - (2 * border)))
                    self.clicking = True
                else:
                    pygame.draw.rect(self.screen, self.active, (self.pos[0] + border, self.pos[1] + (self.size[1] * self.value / float(self.scrollsize)) + border, self.size[0] - (2 * border), self.size[1] ** 2 / self.scrollsize - (2 * border)))
            else:
                pygame.draw.rect(self.screen, self.inactive, (self.pos[0] + border, self.pos[1] + (self.size[1] * self.value / float(self.scrollsize)) + border, self.size[0] - (2 * border), self.size[1] ** 2 / self.scrollsize - (2 * border)))
        else:
            if self.pos[0] <= cur[0] < self.pos[0] + self.size[0] and self.pos[1] <= cur[1] < self.pos[1] + self.size[1] and self.clickable:
                if click:
                    pygame.draw.rect(self.screen, self.activated, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))
                else:
                    pygame.draw.rect(self.screen, self.active, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))
            else:
                pygame.draw.rect(self.screen, self.inactive, (self.pos[0] + border, self.pos[1] + border, self.size[0] - (2 * border), self.size[1] - (2 * border)))

        if self.clicking:
            self.value = (cur[1] - self.pos[1] - (self.size[1] ** 2 / self.scrollsize) / 2) * self.scrollsize / self.size[1]
            if self.value < 0:
                self.value = 0
            elif self.value + self.size[1] >= self.scrollsize:
                self.value = self.scrollsize - self.size[1] - 1

        if not click:
            self.clicking = False

class Textwrap:
    def __init__(self, screen, pos, size, text, font = defaultFont, color = black, textpos = "center"):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.text = text
        self.font = font
        self.color = color
        self.textpos = textpos

    def display(self):
        remaining = self.text + "_"
        displace = 0

        while remaining:
            if self.font.render(remaining[:remaining.find(" ")], True, self.color).get_rect()[2] >= self.size:
                line = ""

                if self.font.render(remaining[0] + "-", True, self.color).get_rect()[2] >= self.size:
                    while remaining[0] == " ":
                        remaining = remaining[1:]
                    line = remaining[0]
                else:
                    while self.font.render(line + remaining[len(line)] + "-", True, self.color).get_rect()[2] < self.size and remaining:
                        line += remaining[len(line)]

                remaining = remaining[len(line):]
                Text(self.screen, (self.pos[0], self.pos[1] + displace), line + "-", font = self.font, color = self.color, textpos = self.textpos).display()
                displace += self.font.render(line, True, self.color).get_rect()[3]
            else:
                line = ""
                
                while self.font.render(line + remaining[:remaining.find(" ")], True, self.color).get_rect()[2] < self.size and remaining:
                    if remaining.find(" ") != -1:
                        line += remaining[:remaining.find(" ") + 1]
                        remaining = remaining[remaining.find(" ") + 1:]
                    else:
                        line += remaining
                        remaining = ""

                Text(self.screen, (self.pos[0], self.pos[1] + displace), line[:-1], font = self.font, color = self.color, textpos = self.textpos).display()
                displace += self.font.render(line, True, self.color).get_rect()[3]

class Textlimit:
    def __init__(self, screen, pos, size, text, font = defaultFont, color = black, textpos = "center"):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.text = text
        self.font = font
        self.color = color
        self.textpos = textpos

    def display(self):
        line = ""

        if self.font.render(self.text, True, self.color).get_rect()[2] < self.size:
            line = self.text
        elif self.font.render(self.text[0] + "...", True, self.color).get_rect()[2] >= self.size:
            line = self.text[0] + "..."
        else:
            while line != self.text and self.font.render(line + self.text[len(line)] + "...", True, self.color).get_rect()[2] < self.size:
                line += self.text[len(line)]
            line += "..."

        Text(self.screen, (self.pos[0], self.pos[1]), line, font = self.font, color = self.color, textpos = self.textpos).display()

def test():
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("PyWL")

    text = Text(screen, (400, 50), "text")
    check = Checkbox(screen, (100, 100), 30)
    button = Button(screen, (200, 100), (100, 50))
    slider = Slider(screen, (400, 100), 30, (1, 270), 135)
    dropdown = Dropdown(screen, (200, 200), (100, 50), ["one", "two", "three", "four"])
    entry = Input(screen, (400, 200), (300, 50))
    window = Window(screen, (100, 400), (200, 200))
    progress = Progress(screen, (400, 300), (200, 30), 0.67)
    scrollbar = Scrollbar(screen, (100, 200), (30, 130), 400)
    textwrap = Textwrap(screen, (400, 400), 100, "This is a short string that is wrapped in a 100 pixel region", textpos = "northwest")
    textlimit = Textlimit(screen, (550, 400), 200, "This string will be cut off after 200 pixels", textpos = "northwest")

    window.widgets.append(Text(screen, (30, 25), "text"))
    window.widgets.append(Checkbox(screen, (60, 10), 30))
    window.widgets.append(Button(screen, (100, 10), (90, 30)))
    window.widgets.append(Slider(screen, (10, 50), 30, (1, 80), 40))
    window.widgets.append(Dropdown(screen, (130, 50), (60, 30), ["one", "two", "three", "four"]))
    window.widgets.append(Input(screen, (10, 90), (110, 30)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)

        text.display()
        check.display()
        button.display()
        slider.display()
        dropdown.display()
        entry.display()
        window.display()
        progress.display()
        scrollbar.display()
        textwrap.display()
        textlimit.display()
        
        pygame.display.flip()

if __name__ == "__main__":
    test()
