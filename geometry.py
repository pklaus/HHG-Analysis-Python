#!/usr/bin/env python
# -*- coding: utf-8 -*-

class coordinates(object):
    """ 2-dimensional coordinates """
    x = None
    y = None
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
    def move(self, offset):
        """ Move the coordinates by offset """
        self.x += offset.x
        self.y += offset.y
    def __add__(self, other):
        """ Vector addition """
        return coordinates(self.x+other.x, self.y+other.y)
class rectangle(object):
    """ A rectangle in 2-dimensional space. """
    def __init__(self, pos = None, dim = None):
        if pos == None: pos = coordinates()
        if dim == None: dim = coordinates()
        self.pos = pos
        """ The position of the rectangle. """
        self.dim = dim
        """ The size (dimensions) of the rectangle. """
    def fully_in(self, other):
        """ Tests if another rectangle lies entierely in this rectangle. """
        if self.pos.x >= other.pos.x and \
           self.pos.y >= other.pos.y and \
           self.pos.x + self.dim.x <= other.pos.y + other.dim.x and \
           self.pos.y + self.dim.y <= other.pos.y + other.dim.y:
               return True
        return False
    def move(self, by):
        """ Move this rectangle to a different position. """
        self.pos.move(by)
    def get_rectangle_inside(self, size, center):
        """
        Create a new rectangle that must be inside this rectangle.
        If it would overlap with this rectangle, it would be moved to the inside.
        """
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
        """ Return a tuple of two corners of the rectangle. """
        return (self.pos, self.pos+self.dim)
