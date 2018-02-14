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
        self.surface = pygame.Surface(size)
        self.occurrence = occurrence
        self.direction = direction
        self.size = size
        self.parent = parent
        self.position = position

        if direction == Direction.LTR or direction == Direction.RTL:
            if self.occurrence < 1 or self.occurrence > self.size[0]:
                self.occurrence = size[0]
        else:
            if self.occurrence < 1 or self.occurrence > self.size[1]:
                self.occurrence = size[1]

        self.set_color(start_color, end_color)

    def gen_rect(self):
        ret = []
        x,y,w,h = 0,0,0,0
        for i in range(self.occurrence):
            if self.direction == Direction.LTR or self.direction == Direction.RTL:
                x, y, w, h = int(self.size[0]//self.occurrence*i), 0, self.size[0]//self.occurrence, self.size[1]
            else:
                x, y, w, h = 0, int(self.size[1]//self.occurrence*i), self.size[0], self.size[1]//self.occurrence

            ret.append((x,y,w,h))
        if self.direction == Direction.BTT or self.direction == Direction.LTR:
            tmp = ret
            for i in range(self.occurrence):
                ret[i] = tmp[-i]
        return ret

    def gen_color(self, start_color, end_color, occurrence, index):
        r_coeff = start_color.r + int((end_color.r - start_color.r)/occurrence*index)
        g_coeff = start_color.g + int((end_color.g - start_color.g)/occurrence*index)
        b_coeff = start_color.b + int((end_color.b - start_color.b)/occurrence*index)
        a_coeff = start_color.a + int((end_color.a - start_color.a)/occurrence*index)
        return pygame.Color(r_coeff,g_coeff,b_coeff,a_coeff)

    def set_color(self,start_color, end_color):
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
