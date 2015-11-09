#! /usr/bin/env python

import logtool
from xxpaper.sheet import Sheet

class Private (Sheet):

  @logtool.log_call (log_args = False)
  def __init__ (self, cfgs, paper, outline, sheet, page, fname):
    super (Private, self).__init__ (cfgs, paper, outline, sheet, page, fname)
    # Offsets within tile
    self.number_stripe_height = float (self.value ("number_stripe_height"))
    self.number_text_inset_x = float (self.value ("number_text_inset_x"))
    self.number_stripe_inset_y = float (self.value ("number_stripe_inset_y"))

  @logtool.log_call
  def page_details (self):
    self.number_stripe ()

  @logtool.log_call
  def tile_details (self, x, y):
    self.title (x, y)
    self.description (x, y)
    self.number_cost (x, y)
    self.number_revenue (x, y)
    self.closes (x, y)

  @logtool.log_call
  def number_stripe (self):
    oy = self.y_off + self.number_stripe_inset_y
    for y in xrange (self.num_y):
      by = (y * self.tile_y) + oy
      self.box ("number", 0, 0, 0, by, self.rubber_x,
                self.number_stripe_height)

  @logtool.log_call
  def number_cost (self, x, y):
    bx = self.number_text_inset_x
    by = self.number_stripe_inset_y + 3
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("cost", x, y, h_centre = -1, v_centre = 1)

  @logtool.log_call
  def number_revenue (self, x, y):
    bx = self.tile_x - self.number_text_inset_x
    by = self.number_stripe_inset_y + 3
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("revenue", x, y, h_centre = 1, v_centre = 1)

  @logtool.log_call
  def title (self, x, y):
    inset_y = float (self.value ("title_inset_y"))
    bx = self.tile_x / 2
    by = self.tile_y - inset_y
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("title", x, y, h_centre = 0, v_centre = 1)

  @logtool.log_call
  def description (self, x, y):
    bx = self.tile_x / 2
    by = (self.number_stripe_inset_y * 2) + self.number_stripe_height
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("desc", x, y, h_centre = 0, v_centre = -1)

  @logtool.log_call
  def closes (self, x, y):
    inset_x = float (self.value ("close_inset_x"))
    inset_y = float (self.value ("close_inset_y"))
    bx = inset_x
    by = self.tile_y - inset_y
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("close", x, y, h_centre = -1, v_centre = 1)
