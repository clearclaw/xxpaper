#! /usr/bin/env python

from xxpaper.sheet import Sheet

class Token (Sheet):
  def __init__ (self, conf, sheet, page, fname):
    Sheet.__init__ (self, conf, sheet, page, fname)
    # Offsets within tile
    self.text_stripe_height = float (self.value ("text_stripe_height"))
    self.token_space_x = float (self.value ("token_space_x"))
    self.token_radius = int (self.value ("token_radius"))
    self.token_inset_y = int (self.value ("token_inset_y"))
    self.token_stripe_angle = int (self.value ("token_stripe_angle"))
    self.token_stripe_text_fudge = float (self.value ("token_stripe_text_fudge"))

  def page_details (self):
    pass

  def tile_details (self, x, y):
    self.top_stripe (x, y)
    self.bottom_stripe (x, y)
    self.text_stripe (x, y)
    self.token_circles (x, y)

  def top_stripe (self, x, y):
    bx = self.tile_x
    by = self.tile_y / 2
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("token_top_colour",x ,y))
    self.fd.append ("%d %d %d %d rectfill" % (0, 0, bx, by))
    self.fd.append ("grestore")

  def bottom_stripe (self, x, y):
    bx = self.tile_x
    by = float (self.tile_y / 2)
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("token_bottom_colour", x, y))
    self.fd.append ("%f %f %f %f rectfill"
                    % (0, self.tile_y / 2,
                       bx, self.tile_y / 2))
    self.fd.append ("grestore")

  def text_stripe (self, x, y):
    bx = self.tile_x
    by = self.text_stripe_height
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("text_stripe_colour", x, y))
    self.fd.append ("%f %f %f %f rectfill"
                    % (0, float (self.tile_y / 2) - float (self.text_stripe_height / 2),
                       bx, by))
    self.fd.append ("0 setgray")
    self.fd.append ("0.3 setlinewidth")
    self.fd.append ("%f %f %f %f rectstroke"
                    % (0, float (self.tile_y / 2) - float (self.text_stripe_height / 2),
                       bx, by))
    self.fd.append ("grestore")

  def token_circles (self, x, y):
    ox = self.token_space_x
    oy = float (self.tile_y / 2)
    spacing = self.token_space_x + (self.token_radius * 2)
    count = int (self.value ("token_count", x, y))
    self.fd.append ("gsave")
    for i in xrange (1, count + 1):
      bx = ox + (i * spacing)
      by = oy
      self.fd.append ("%f %f moveto" % (bx, by))
      self.company_token (x, y)
    self.fd.append ("grestore")
