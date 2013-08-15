#! /usr/bin/env python

from xxpaper.sheet import Sheet
from types import StringType

class Private (Sheet):
  def __init__ (self, conf, sheet, page, fname):
    Sheet.__init__ (self, conf, sheet, page, fname)
    # Offsets within tile
    self.number_stripe_height = int (self.value ("number_stripe_height"))
    self.number_text_inset_x = int (self.value ("number_text_inset_x"))
    self.number_stripe_inset_y = int (self.value ("number_stripe_inset_y"))
    self.title_inset_y = int (self.value ("title_inset_y"))
    self.title_line_height = int (self.value ("title_line_height"))
    self.desc_line_height = int (self.value ("desc_line_height"))
    self.close_text_inset_x = int (self.value ("close_text_inset_x"))
    self.close_text_inset_y = int (self.value ("close_text_inset_y"))

  def page_details (self):
    self.number_stripe ()

  def tile_details (self, x, y):
    self.title (x, y)
    self.description (x, y)
    self.number_cost (x, y)
    self.number_revenue (x, y)
    self.closes (x, y)

  def number_stripe (self):
    oy = self.y_off + self.number_stripe_inset_y
    for y in xrange (self.num_y):
      if self.value ("number_colour", 0, y):
        by = (y * self.tile_y) + oy
        self.fd.append ("%s %s %s setrgbcolor"
                        % self.value ("number_colour", 0, y))
        self.fd.append ("0 %d %d %d rectfill"
                        % (by, self.rubber_x, self.number_stripe_height))

  def number_cost (self, x, y):
    bx = self.number_text_inset_x
    by = self.number_stripe_inset_y + 3
    self.fd.append ("/%s %s selectfont" % self.value ("number_font", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("number_text_colour", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) show" % self.value ("number_cost", x, y))

  def number_revenue (self, x, y):
    bx = self.tile_x - self.number_text_inset_x
    by = self.number_stripe_inset_y + 3
    self.fd.append ("/%s %s selectfont" % self.value ("number_font", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("number_text_colour", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) dup stringwidth pop neg 0 rmoveto show"
                    % self.value ("number_revenue", x, y))

  def title (self, x, y):
    bx = self.tile_x / 2
    by = self.tile_y - self.title_inset_y
    self.fd.append ("%d %d moveto" % (bx, by))
    self.text ("title", x, y, h_centre = 0, v_centre = 1)

  def description (self, x, y):
    bx = self.tile_x / 2
    by = (self.number_stripe_inset_y * 2) + self.number_stripe_height
    self.fd.append ("%d %d moveto" % (bx, by))
    self.text ("desc", x, y, h_centre = 0, v_centre = -1)

  def closes (self, x, y):
    bx = self.close_text_inset_x
    by = self.tile_y - self.close_text_inset_y
    self.fd.append ("/%s %s selectfont" % self.value ("close_font", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("close_text_colour", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) show" % self.value ("close", x, y))
