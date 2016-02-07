#! /usr/bin/env python

import logtool
from xxpaper.sheet import Sheet

class Market (Sheet):

  @logtool.log_call
  def page_details (self):
    pass

  @logtool.log_call
  def tile_details (self, x, y):
    self.type_desc (x, y)

  @logtool.log_call
  def type_desc (self, x, y):
    desc_pos = self.value ("desc_position", x, y)
    bx = self.tile_x / 2
    by = self.tile_y / 10
    if "bottom" in desc_pos:
      self.fd.append ("gsave")
      self.fd.append ("%f %f moveto" % (bx, by))
      self.text ("desc", x, y, h_centre = 0, v_centre = -1)
      self.fd.append ("grestore")
    bx = self.tile_x / 2
    by = 9 * self.tile_y / 10
    if "top" in desc_pos:
      self.fd.append ("gsave")
      self.fd.append ("%f %f moveto" % (bx, by))
      self.fd.append ("180 rotate")
      self.text ("desc", x, y, h_centre = 0, v_centre = -1)
      self.fd.append ("grestore")
