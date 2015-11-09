#! /usr/bin/env python

import logtool
from xxpaper.sheet import Sheet

class Market15 (Sheet):

  @logtool.log_call
  def page_details (self):
    pass

  @logtool.log_call
  def tile_details (self, x, y):
    self.type_desc (x, y)

  @logtool.log_call
  def type_desc (self, x, y):
    bx = self.tile_x / 2
    by = self.tile_y / 10
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("desc", x, y, h_centre = 0, v_centre = -1)
    self.fd.append ("grestore")
    bx = self.tile_x / 2
    by = 9 * self.tile_y / 10
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (bx, by))
    self.fd.append ("180 rotate")
    self.text ("desc", x, y, h_centre = 0, v_centre = -1)
    self.fd.append ("grestore")

  @logtool.log_call
  def tile_block (self):
    ox = self.x_off
    oy = self.y_off
    half_ox = int (self.tile_x / 2)
    for x in xrange (self.num_x):
      for y in xrange (self.num_y):
        bx = (x * self.tile_x) + ox + ((y % 2) * half_ox)
        by = (y * self.tile_y) + oy
        self.push_tile (x, y, bx, by)
        self.tile_details (x, y)
        self.pop_tile ()
