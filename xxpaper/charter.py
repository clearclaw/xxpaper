#! /usr/bin/env python

import logtool
from xxpaper.sheet import Sheet

class Charter (Sheet):

  @logtool.log_call (log_args = False)
  def __init__ (self, cfgs, paper, outline, sheet, page, fname):
    super (Charter, self).__init__ (cfgs, paper, outline, sheet, page, fname)
    # Offsets within tile
    self.box_inset_x = float (self.value ("box_inset_x"))
    self.box_inset_y = float (self.value ("box_inset_y"))
    self.box_radius = float (self.value ("box_radius"))
    self.stripe_height = float (self.value ("stripe_height"))
    self.stripe_radius = float (self.value ("stripe_radius"))
    self.title_inset_x = float (self.value ("title_inset_x"))

  @logtool.log_call
  def page_details (self):
    self.macro_roundbox ()

  @logtool.log_call
  def tile_details (self, x, y):
    self.charter_box (x, y)
    self.charter_stripe (x, y)
    self.centre_stripe (x, y)
    self.charter_stripe_token (x, y)
    self.title (x, y)
    self.token_circles (x, y)
    self.desc1 (x, y)
    self.desc2 (x, y)
    self.note1 (x, y)
    self.note2 (x, y)

  @logtool.log_call
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

  @logtool.log_call
  def charter_box (self, x, y):
    bx = self.box_inset_x
    by = self.box_inset_y
    self.fd.append ("%f %f moveto" % (bx, by))
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (bx, by))
    self.fd.append ("currentpoint translate")
    self.fd.append ("%f %f %f roundbox"
                    % (self.tile_x - (self.box_inset_x * 2),
                       self.tile_y - (self.box_inset_y * 2),
                       self.box_radius))
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor" % self.value ("box_colour", x, y))
    self.fd.append ("fill")
    self.fd.append ("grestore")
    self.fd.append ("%s setlinewidth" % self.value ("box_stroke", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("box_stroke_colour", x, y))
    self.fd.append ("stroke")
    self.fd.append ("grestore")

  @logtool.log_call
  def charter_stripe (self, x, y):
    bx = self.box_inset_x
    by = self.tile_y - self.box_inset_y - self.stripe_height
    self.fd.append ("%f %f moveto" % (bx, by))
    self.fd.append ("gsave")
    self.fd.append ("currentpoint translate")
    self.fd.append ("%f %f %f roundbox"
                    % (self.tile_x - (self.box_inset_x * 2),
                       self.stripe_height,
                       self.stripe_radius))
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("stripe_colour", x, y))
    self.fd.append ("fill")
    self.fd.append ("grestore")
    self.fd.append ("%s setlinewidth" % self.value ("stripe_stroke", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("stripe_stroke_colour", x, y))
    self.fd.append ("closepath")
    self.fd.append ("stroke")
    self.fd.append ("grestore")

  @logtool.log_call
  def charter_stripe_token (self, x, y):
    bx = self.box_inset_x + self.stripe_radius
    by = self.tile_y - self.box_inset_y - self.stripe_radius
    self.fd.append ("%f %f moveto" % (bx, by))
    self.company_token (x, y)

  @logtool.log_call
  def title (self, x, y):
    title_inset_y_fudge = float (self.value ("title_inset_y_fudge", x, y))
    bx = (self.box_inset_x + ((self.tile_x - (self.box_inset_x * 2)) / 2)
          + self.title_inset_x)
    by = (self.tile_y - self.box_inset_x - self.box_radius
          - title_inset_y_fudge)
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("title", x, y, h_centre = 0, v_centre = 0)
    self.fd.append ("grestore")

  @logtool.log_call
  def token_circles (self, x, y):
    token_inset_x = float (self.value ("token_inset_x", x, y))
    token_inset_y = float (self.value ("token_inset_y", x, y))
    token_radius = float (self.value ("token_radius", x, y))
    ox = (self.box_inset_x
          + token_inset_x + token_radius)
    oy = (self.tile_y - self.box_inset_y - self.stripe_height
          - token_inset_y)
    gap = oy - token_inset_y - token_radius / 2
    count = int (self.value ("token_count", x, y))
    token_spacing = int (self.value ("charter_token_spacing", x))
    spacing = gap / token_spacing if token_spacing else gap / (count + 1)
    self.fd.append ("gsave")
    for i in xrange (1, count + 1):
      bx = ox
      by = oy - (i * spacing)
      self.fd.append ("%f %f moveto" % (bx, by))
      self.company_token_circle (x, y)
      price_height_fudge = float (self.value ("price%s_height_fudge" % i, x, y))
      self.fd.append ("%f %f moveto" % (bx, by - price_height_fudge))
      self.text ("price%s" % i, x, y, h_centre = 0, v_centre = 0)
    self.fd.append ("grestore")

  @logtool.log_call
  def centre_stripe (self, x, y):
    bx = self.tile_x / 2
    by = self.box_inset_y
    h = self.tile_y - by - self.box_inset_y - self.stripe_height
    self.line ("centre", x, y, bx, by, 0, h)

  @logtool.log_call
  def desc1 (self, x, y):
    centre = self.value ("centre_colour", x, y)
    if centre == "transparent":
      bx = self.tile_x / 2
    else:
      bx = self.tile_x / 4
    by = (self.tile_y - self.box_inset_y - self.box_radius
          - self.stripe_height)
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("desc1", x, y, h_centre = 0, v_centre = 0)
    self.fd.append ("grestore")

  @logtool.log_call
  def desc2 (self, x, y):
    centre = self.value ("centre_colour", x, y)
    if centre == "transparent":
      return
    bx = (self.tile_x * 3) / 4
    by = (self.tile_y - self.box_inset_y - self.box_radius
          - self.stripe_height)
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("desc2", x, y, h_centre = 0, v_centre = 0)
    self.fd.append ("grestore")

  @logtool.log_call
  def note1 (self, x, y):
    centre = self.value ("centre_colour", x, y)
    if centre == "transparent":
      bx = self.tile_x / 2
    else:
      bx = self.tile_x / 4
    by = self.box_inset_y + (self.box_radius / 2)
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("note1", x, y, h_centre = 0, v_centre = -1)
    self.fd.append ("grestore")

  @logtool.log_call
  def note2 (self, x, y):
    centre = self.value ("centre_colour", x, y)
    if centre == "transparent":
      return # No second side
    bx = (self.tile_x * 3) / 4
    by = self.box_inset_y + (self.box_radius / 2)
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("note2", x, y, h_centre = 0, v_centre = -1)
    self.fd.append ("grestore")
