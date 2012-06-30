#!/usr/bin/env python

class coordinates(object):
    x = None
    y = None
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
    def move(self, offset):
        self.x += offset.x
        self.y += offset.y
    def __add__(self, other):
        return coordinates(self.x+other.x, self.y+other.y)
class rectangle(object):
    pos = coordinates()
    dim = coordinates()
    def fully_in(self, other):
        if self.pos.x >= other.pos.x and \
           self.pos.y >= other.pos.y and \
           self.pos.x + self.dim.x <= other.pos.y + other.dim.x and \
           self.pos.y + self.dim.y <= other.pos.y + other.dim.y:
               return True
        return False
    def move(self, by):
        self.pos.move(by)
    def get_rectangle_inside(self, size, center):
        box = rectangle()
        box.pos.x = center.x - size/2
        box.pos.y = center.y - size/2
        box.dim.x, box.dim.y = size, size
        if  box.pos.x < self.pos.x:
            box.move(coordinates(self.pos.x - box.pos.x, 0))
        if  box.pos.y < self.pos.y:
            box.move(coordinates(0, self.pos.y - box.pos.y))
        if  box.pos.x + box.dim.x > self.pos.x + self.dim.x:
            box.move(coordinates(self.pos.x + self.dim.x - (box.pos.x + box.dim.x), 0))
        if  box.pos.y + box.dim.y > self.pos.y + self.dim.y:
            box.move(coordinates(0, self.pos.y + self.dim.y - (box.pos.y + box.dim.y)))
        if not box.fully_in(self):
            raise NameError("Box too big for me.")
        return box
    def corners(self):
        return (self.pos, self.pos+self.dim)
