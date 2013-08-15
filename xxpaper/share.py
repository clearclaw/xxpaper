#! /usr/bin/env python

from xxpaper.sheet import Sheet
from types import StringType

class Share (Sheet):
  def __init__ (self, conf, sheet, page, fname):
    Sheet.__init__ (self, conf, sheet, page, fname)
    # Offsets within tile
    self.side_stripe_inset_x = int (self.value ("side_stripe_inset_x"))
    self.side_stripe_width = int (self.value ("side_stripe_width"))
    self.title_inset_x = int (self.value ("title_inset_x"))
    self.title_inset_y = int (self.value ("title_inset_y"))
    self.title_line_height = int (self.value ("title_line_height"))
    self.token_radius = int (self.value ("token_radius"))
    self.token_inset_y = int (self.value ("token_inset_y"))
    self.token_stripe_angle = int (self.value ("token_stripe_angle"))
    self.token_stripe_text_fudge = float (self.value ("token_stripe_text_fudge"))
    self.type_desc_inset_x = int (self.value ("type_desc_inset_x"))
    self.type_note_inset_x = int (self.value ("type_note_inset_x"))
    self.type_stripe_height = int (self.value ("type_stripe_height"))
    self.type_stripe_inset_x = int (self.value ("type_stripe_inset_x"))
    self.type_stripe_inset_y = int (self.value ("type_stripe_inset_y"))
    self.type_stripe_inset_y_fudge = float (self.value ("type_stripe_inset_y_fudge"))
    self.type_stripe_width = self.x_off + self.tile_x - self.type_stripe_inset_x

  def page_details (self):
    self.side_stripe ()
    self.type_stripe ()

  def tile_details (self, x, y):
    self.type_size (x, y)
    self.type_note (x, y)
    self.type_desc (x, y)
    self.tokens (x, y)
    self.title (x, y)

  def side_stripe (self):
    ox = self.x_off + self.side_stripe_inset_x
    for x in xrange (self.num_x):
      bx = (self.tile_x * x) + ox
      self.fd.append ("%s %s %s setrgbcolor"
                      % self.value ("stripe_colour", x, 0))
      self.fd.append ("%d 0 %d %d rectfill" % (bx, self.side_stripe_width,
                                               self.rubber_y))

  def type_stripe (self):
    oy = self.y_off + self.type_stripe_inset_y
    for y in xrange (self.num_y):
      if self.value ("type_colour", 0, y):
        by = (y * self.tile_y) + oy
        self.fd.append ("%s %s %s setrgbcolor"
                        % self.value ("type_colour", 0, y))
        self.fd.append ("0 %d %d %d rectfill"
                        % (by, self.type_stripe_width, self.type_stripe_height))

  def type_size (self, x, y):
    bx = self.side_stripe_inset_x + (self.side_stripe_width / 2)
    by = self.type_stripe_inset_y + self.type_stripe_inset_y_fudge
    self.fd.append ("/%s %s selectfont" % self.value ("type_font", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("type_text_colour", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) dup stringwidth pop 2 div neg 0 rmoveto show"
                    % self.value ("type_size", x, y))

  def type_note (self, x, y):
    bx = (self.side_stripe_inset_x + self.side_stripe_width
          + self.type_note_inset_x)
    by = self.type_stripe_inset_y + self.type_stripe_inset_y_fudge
    if self.value ("type_note", x, y):
      self.fd.append ("/%s %s selectfont" % self.value ("type_font", x, y))
      self.fd.append ("%s %s %s setrgbcolor"
                      % self.value ("type_text_colour", x, y))
      self.fd.append ("%d %d moveto" % (bx, by))
      self.fd.append ("(%s) show" % self.value ("type_note", x, y))

  def type_desc (self, x, y):
    bx = self.type_stripe_width - self.type_desc_inset_x - self.x_off
    by = self.type_stripe_inset_y + self.type_stripe_inset_y_fudge
    self.fd.append ("/%s %s selectfont" % self.value ("type_font", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("type_text_colour", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) dup stringwidth pop neg 0 rmoveto show"
                    % self.value ("type_desc", x, y))

  def tokens (self, x, y):
    ox = self.side_stripe_inset_x + (self.side_stripe_width / 2)
    oy = self.type_stripe_inset_y + self.type_stripe_height + self.token_inset_y
    gap = self.tile_y - oy - self.token_inset_y
    count = int (self.value ("token_count", x, y))
    spacing = gap / (count + 1)
    for i in xrange (1, count + 1):
      bx = ox
      by = oy + (i * spacing)
      self.fd.append ("%d %d moveto" % (bx, by))
      self.company_token (x, y)

  def title (self, x, y):
    o = (self.side_stripe_inset_x + self.side_stripe_width
         + self.title_inset_x)
    w = self.tile_x - o
    bx = (o + (w / 2))
    by = self.tile_y - self.title_inset_y
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("title", x, y, h_centre = 0, v_centre = 1)
