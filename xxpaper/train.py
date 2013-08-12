#! /usr/bin/env python

from xxpaper.sheet import Sheet

class Train (Sheet):
  def __init__ (self, conf, sheet, page, fname):
    Sheet.__init__ (self, conf, sheet, page, fname)
    # Offsets within tile
    self.rust_stripe_inset_y = 5
    self.rust_stripe_height = 13
    self.train_type_inset_y = 70

  def page_details (self):
    self.rust_stripe ()
    self.trade_stripe ()

  def tile_details (self, x, y):
    self.train_type (x, y)
    self.rust_by (x, y)
    self.trade_to (x, y)
    self.train_cost (x, y)

  def train_cost (self, x, y):
    bx = self.tile_x / 2
    by = self.rust_stripe_inset_y + (self.rust_stripe_height * 4)
    self.fd.append ("/%s %s selectfont"
                    % self.value ("train_cost_font", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("train_cost_colour", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) dup stringwidth pop 2 div neg 0 rmoveto show"
                    % self.value ("cost", x, y))

  def trade_to (self, x, y):
    bx = self.tile_x / 2
    by = (self.rust_stripe_inset_y * 2) + self.rust_stripe_height + 3
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("train_trade_colour", x, y))
    self.fd.append ("/%s %s selectfont"
                    % self.value ("train_trade_font", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) dup stringwidth pop 2 div neg 0 rmoveto show"
                    % self.value ("trade", x, y))

  def trade_stripe (self):
    oy = self.y_off + (self.rust_stripe_inset_y * 2) + self.rust_stripe_height
    for y in xrange (self.num_y):
      by = (y * self.tile_y) + oy
      self.fd.append ("%s %s %s setrgbcolor"
                      % self.value ("trade_colour", 0, y))
      self.fd.append ("0 %d %d %d rectfill"
                      % (by, self.rubber_x, self.rust_stripe_height))

  def rust_by (self, x, y):
    bx = self.tile_x / 2
    by = self.rust_stripe_inset_y + 2
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("train_rust_colour", x, y))
    self.fd.append ("/%s %s selectfont"
                    % self.value ("train_rust_font", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) dup stringwidth pop 2 div neg 0 rmoveto show"
                    % self.value ("rust_by", x, y))

  def rust_stripe (self):
    oy = self.y_off + self.rust_stripe_inset_y
    for y in xrange (self.num_y):
      by = (y * self.tile_y) + oy
      self.fd.append ("%s %s %s setrgbcolor"
                      % self.value ("rust_colour", 0, y))
      self.fd.append ("0 %d %d %d rectfill"
                      % (by, self.rubber_x, self.rust_stripe_height))

  def train_type (self, x, y):
    bx = self.tile_x / 2
    by = self.tile_y - self.train_type_inset_y
    self.fd.append ("/%s %s selectfont"
                    % self.value ("train_type_font", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("train_type_colour", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) dup stringwidth pop 2 div neg 0 rmoveto show"
                    % self.value ("type", x, y))
