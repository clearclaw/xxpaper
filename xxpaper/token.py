#! /usr/bin/env python

import math
from xxpaper.sheet import Sheet

class Token (Sheet):
  def __init__ (self, cfgs, sheet, page, fname):
    Sheet.__init__ (self, cfgs, sheet, page, fname)

  def tile_details (self, x, y):
    self.top (x, y)
    self.top_stripe (x, y)
    self.bottom (x, y)
    self.bottom_stripe (x, y)
    self.text_stripe (x, y)
    self.token_circles (x, y)

  def bottom (self, x, y):
    bx = self.tile_x
    by = self.tile_y / 2
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("token_bottom_colour",x ,y))
    self.fd.append ("%d %d %d %d rectfill" % (0, 0, bx, by))
    self.fd.append ("grestore")

  def bottom_stripe (self, x, y):
    stripe_colour = self.value ("token_bottom_stripe_colour", x, y)
    if stripe_colour == "transparent":
      return
    bx = self.tile_x
    by = self.tile_y / 2
    radius = float (self.value ("token_radius", x, y))
    angle = float (self.value ("token_bottom_stripe_angle", x, y))
    height = math.sin (math.radians (angle)) * radius
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor" % stripe_colour)
    self.fd.append ("%f %f %f %f rectfill"
                    % (0, 0,
                       bx, (self.tile_y / 2) - height,))
    self.fd.append ("grestore")

  def top (self, x, y):
    bx = self.tile_x
    # by = float (self.tile_y / 2)
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("token_top_colour", x, y))
    self.fd.append ("%f %f %f %f rectfill"
                    % (0, self.tile_y / 2,
                       bx, self.tile_y / 2))
    self.fd.append ("grestore")

  def top_stripe (self, x, y):
    stripe_colour = self.value ("token_top_stripe_colour", x, y)
    if stripe_colour == "transparent":
      return
    bx = self.tile_x
    # by = float (self.tile_y / 2)
    radius = float (self.value ("token_radius", x, y))
    angle = float (self.value ("token_top_stripe_angle", x, y))
    height = math.sin (math.radians (angle)) * radius
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor" % stripe_colour)
    self.fd.append ("%f %f %f %f rectfill"
                    % (0, (self.tile_y / 2) + height,
                       bx, self.tile_y / 2,))
    self.fd.append ("grestore")

  def text_stripe (self, x, y):
    stroke = float (self.value ("token_stroke"))
    stroke_colour = self.value ("token_stroke_colour")
    stripe_height = float (self.value ("text_stripe_height"))
    bx = self.tile_x
    by = stripe_height
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("token_colour", x, y))
    self.fd.append ("%f %f %f %f rectfill"
                    % (0, float (self.tile_y / 2) - (stripe_height / 2),
                       bx, by))
    self.fd.append ("%s %s %s setrgbcolor" % stroke_colour)
    self.fd.append ("%f setlinewidth" % stroke)
    self.fd.append ("%f %f %f %f rectstroke"
                    % (0, float (self.tile_y / 2) - (stripe_height / 2),
                       bx, by))
    self.fd.append ("grestore")

  def token_circles (self, x, y):
    space_x = float (self.value ("token_space_x"))
    radius = float (self.value ("token_radius"))
    ox = space_x
    oy = float (self.tile_y / 2)
    spacing = space_x + (radius * 2)
    count = int (self.value ("token_count", x, y))
    self.fd.append ("gsave")
    for i in xrange (1, count + 1):
      bx = ox + (i * spacing)
      by = oy
      self.fd.append ("%f %f moveto" % (bx, by))
      self.company_token (x, y)
    self.fd.append ("grestore")
