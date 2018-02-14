import pygame
import enum
import time

class Direction(enum.Enum):
    LTR = 0
    RTL = 1
    TTB = 2
    BTT = 3

class Gradient():
    def __init__(self, parent, position, size, start_color = pygame.Color(0,0,0), end_color = pygame.Color(255,255,255), direction = Direction.LTR, occurrence = -1):
        self.occurrence = occurrence
        self.direction = direction
        self.parent = parent
        self.position = position
        self.start_color = start_color
        self.end_color = end_color
        print(size)

        self.resize(size)

    def resize(self, size):
        self.surface = pygame.Surface(size)
        self.size = size
        if self.direction == Direction.LTR or self.direction == Direction.RTL:
            if self.occurrence < 1 or self.occurrence > self.size[0]:
                self.occurrence = size[0]
        else:
            if self.occurrence < 1 or self.occurrence > self.size[1]:
                self.occurrence = size[1]
        self.set_color(self.start_color, self.end_color)

    def gen_rect(self):
        ret = []
        print(self.surface.get_width(),self.surface.get_height())
        print(self.surface.get_height(),"/",self.occurrence, '=', self.surface.get_height() / self.occurrence)
        x,y,w,h = 0,0,0,0
        for i in range(self.occurrence):
            if self.direction == Direction.TTB or self.direction == Direction.BTT:
                if i != self.occurrence // 2:
                    h = int(self.surface.get_height()/self.occurrence)
                else:
                    h = int(self.surface.get_height()/self.occurrence)+(self.surface.get_height()%self.occurrence)
                w = self.surface.get_width()
                x = 0
                ret.append((x,y,w,h))
                y = y + h
            else:
                if i != self.occurrence // 2:
                    w = int(self.surface.get_width()/self.occurrence)
                else:
                    w = int(self.surface.get_width()/self.occurrence)+(self.surface.get_width()%self.occurrence)
                h = self.surface.get_height()
                y = 0
                ret.append((x,y,w,h))
                x = x + w
        if self.direction == Direction.BTT or self.direction == Direction.LTR:
            tmp = ret
            ret = []
            for i in range(self.occurrence-1,-1,-1):
                ret.append(tmp[i])
        return ret

    def gen_color(self, start_color, end_color, occurrence, index):
        r_coeff = start_color.r + int((end_color.r - start_color.r)/occurrence*index)
        g_coeff = start_color.g + int((end_color.g - start_color.g)/occurrence*index)
        b_coeff = start_color.b + int((end_color.b - start_color.b)/occurrence*index)
        a_coeff = start_color.a + int((end_color.a - start_color.a)/occurrence*index)
        return pygame.Color(r_coeff,g_coeff,b_coeff,a_coeff)

    def set_color(self,start_color, end_color):
        self.start_color = start_color
        self.end_color = end_color
        rects = self.gen_rect()
        for i in range(len(rects)):
            color = self.gen_color(start_color,end_color,self.occurrence,i)
            rect = rects[i]
            self.surface.fill(color,rect)
        self.parent.blit(self.surface,self.position)
        pygame.display.flip()

class GradientAnimation:
    def __init__(self, parent, position, size, start_timestart_color = pygame.Color(0,0,0), end_timestart_color = pygame.Color(255,255,255), start_timeend_color = pygame.Color(0,0,0), end_timeend_color = pygame.Color(255,255,255), duration = 5, direction = Direction.LTR, occurrence = -1, framerate = 25):
        self.gradient = Gradient(parent, position, size, start_timestart_color, end_timestart_color, direction, occurrence)
        self.waittime = 1 / framerate
        self.passes = duration * framerate
        self.actual = 0
        self.actual_time = time.clock()
        self.start_timestart_color = start_timestart_color
        self.start_timeend_color = start_timeend_color
        self.end_timestart_color = end_timestart_color
        self.end_timeend_color = end_timeend_color

    def gen_color(self, start_color, end_color, occurrence, index):
        r_coeff = start_color.r + int((end_color.r - start_color.r)/occurrence*index)
        g_coeff = start_color.g + int((end_color.g - start_color.g)/occurrence*index)
        b_coeff = start_color.b + int((end_color.b - start_color.b)/occurrence*index)
        a_coeff = start_color.a + int((end_color.a - start_color.a)/occurrence*index)
        return pygame.Color(r_coeff,g_coeff,b_coeff,a_coeff)

    def update_color(self):
        if (self.actual_time + self.waittime <= time.clock() and self.actual < self.passes):
            self.actual = self.actual + 1
            self.actual_time =  + self.waittime
            self.gradient.set_color(self.gen_color(self.start_timestart_color, self.start_timeend_color, self.passes, self.actual),
                                    self.gen_color(self.end_timestart_color, self.end_timeend_color, self.passes, self.actual))
