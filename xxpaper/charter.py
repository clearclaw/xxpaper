#! /usr/bin/env python

from xxpaper.sheet import Sheet

class Charter (Sheet):
  def __init__ (self, conf, sheet, page, fname):
    Sheet.__init__ (self, conf, sheet, page, fname)
    # Offsets within tile
    self.box_inset_x = int (self.value ("box_inset_x"))
    self.box_inset_y = int (self.value ("box_inset_y"))
    self.box_corner_radius = int (self.value ("box_corner_radius"))
    self.stripe_height = int (self.value ("stripe_height"))
    self.stripe_corner_radius = int (self.value ("stripe_corner_radius"))
    self.title_inset_y_fudge = int (self.value ("title_inset_y_fudge"))
    self.title_inset_x = int (self.value ("title_inset_x"))
    self.stripe_line_width = int (self.value ("stripe_line_width"))
    self.token_inset_x = int (self.value ("token_inset_x"))
    self.token_inset_y = int (self.value ("token_inset_y"))
    self.token_radius = int (self.value ("token_radius"))
    self.note_inset_x_fudge = int (self.value ("note_inset_x_fudge"))
    self.note_inset_y_fudge = int (self.value ("note_inset_y_fudge"))
    self.desc_inset_x = (self.box_inset_x + (self.token_inset_x * 2)
                         + (self.token_radius * 2))
    self.desc_inset_y = (self.box_inset_y + self.stripe_height + 30)

  def page_details (self):
    self.macro_roundbox ()

  def tile_details (self, x, y):
    self.charter_box (x, y)
    self.charter_stripe (x, y)
    self.charter_stripe_token (x, y)
    self.title (x, y)
    self.token_circles (x, y)
    self.desc (x, y)
    self.note (x, y)

  def macro_roundbox (self):
    self.fd.define (
      "roundbox",
      """
%%Title: Roundbox
% Devised in 2000 by George Spowart
% http://compgroups.net/comp.lang.postscript/how-to-draw-rectangles-with-rounded-corn/1828790
%/roundbox {
/radius exch def
/height exch def
/width exch def
0 radius moveto
0 height width height radius arcto 4 {pop} repeat
width height width 0 radius arcto 4 {pop} repeat
width 0 0 0 radius arcto 4 {pop} repeat
0 0 0 height radius arcto 4 {pop} repeat
closepath
% } def
""")

  def charter_box (self, x, y):
    bx = self.box_inset_x
    by = self.box_inset_y
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("gsave")
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("currentpoint translate")
    self.fd.append ("%d %d %f roundbox"
                    % (self.tile_x - (self.box_inset_x * 2),
                       self.tile_y - (self.box_inset_y * 2),
                       self.box_corner_radius))
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor" % self.value ("box_colour"))
    self.fd.append ("fill")
    self.fd.append ("grestore")
    self.fd.append ("%s setlinewidth" % self.value ("box_line_width"))
    self.fd.append ("%s %s %s setrgbcolor" % self.value ("box_line_colour"))
    self.fd.append ("stroke")
    self.fd.append ("grestore")

  def charter_stripe (self, x, y):
    bx = self.box_inset_x
    by = self.tile_y - self.box_inset_y - self.stripe_height
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("gsave")
    self.fd.append ("currentpoint translate")
    self.fd.append ("%d %d %f roundbox"
                    % (self.tile_x - (self.box_inset_x * 2),
                       self.stripe_height,
                       self.stripe_corner_radius))
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor" % self.value ("stripe_colour", x, y))
    self.fd.append ("fill")
    self.fd.append ("grestore")
    self.fd.append ("%s setlinewidth" % self.value ("stripe_line_width"))
    self.fd.append ("%s %s %s setrgbcolor" % self.value ("stripe_line_colour"))
    self.fd.append ("closepath")
    self.fd.append ("stroke")
    self.fd.append ("grestore")

  def charter_stripe_token (self, x, y):
    bx = self.box_inset_x + self.stripe_corner_radius
    by = self.tile_y - self.box_inset_y - self.stripe_corner_radius
    self.fd.append ("%d %d moveto" % (bx, by))
    self.company_token (x, y)

  def title (self, x, y):
    bx = (self.box_inset_x + ((self.tile_x - (self.box_inset_x * 2)) / 2)
          + self.title_inset_x)
    by = (self.tile_y - self.box_inset_x - self.box_corner_radius
          - self.title_inset_y_fudge)
    self.fd.append ("gsave")
    self.fd.append ("%d %d moveto" % (bx, by))
    self.text ("title", x, y, h_centre = 0, v_centre = 0)
    self.fd.append ("grestore")

  def token_circles (self, x, y):
    ox = (self.box_inset_x
          + self.token_inset_x + self.token_radius)
    oy = (self.tile_y - self.box_inset_x - self.stripe_height
          - self.token_inset_y)
    gap = oy - self.token_inset_y
    count = int (self.value ("token_count", x, y))
    spacing = gap / (count + 1)
    self.fd.append ("gsave")
    for i in xrange (1, count + 1):
      bx = ox
      by = oy - (i * spacing)
      self.fd.append ("%d %d moveto" % (bx, by))
      self.company_token_circle (x, y)
    self.fd.append ("grestore")

  def desc (self, x, y):
    bx = (self.box_inset_x + ((self.tile_x - (self.box_inset_x * 2)) / 2)
          + self.title_inset_x)
    by = (self.tile_y - self.box_inset_y - self.box_corner_radius
          - self.stripe_height)
    self.fd.append ("gsave")
    self.fd.append ("%d %d moveto" % (bx, by))
    self.text ("desc", x, y, h_centre = 0, v_centre = 0)
    self.fd.append ("grestore")

  def note (self, x, y):
    bx = (self.box_inset_x + ((self.tile_x - (self.box_inset_x * 2)) / 2)
          + self.title_inset_x + self.note_inset_x_fudge)
    by = self.box_inset_y + self.box_corner_radius
    self.fd.append ("gsave")
    self.fd.append ("%d %d moveto" % (bx, by))
    self.text ("note", x, y, h_centre = 0, v_centre = -1)
    self.fd.append ("grestore")
