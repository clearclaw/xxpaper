#! /usr/bin/env python

from xxpaper.sheet import Sheet
from types import StringType

class Share (Sheet):
  def __init__ (self, conf, sheet, page, fname):
    Sheet.__init__ (self, conf, sheet, page, fname)
    # Offsets within tile
    self.side_stripe_inset_x = 5
    self.side_stripe_width = 30
    self.type_stripe_height = 10
    self.type_stripe_width = self.x_off + self.tile_x - 10
    self.type_note_inset_x = 10
    self.type_stripe_inset_y = 5
    self.title_inset_x = 5
    self.title_inset_y = 20
    self.title_line_height = 13
    self.type_desc_inset_x = 5
    self.token_inset_y = 5
    self.token_stripe_width = 10

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
    by = self.type_stripe_inset_y + 2.75
    self.fd.append ("/%s %s selectfont" % self.value ("type_font", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("type_text_colour", x, y))
    self.fd.append ("%d %d moveto" % (bx, by))
    self.fd.append ("(%s) dup stringwidth pop 2 div neg 0 rmoveto show"
                    % self.value ("type_size", x, y))

  def type_note (self, x, y):
    bx = (self.side_stripe_inset_x + self.side_stripe_width
          + self.type_note_inset_x)
    by = self.type_stripe_inset_y + 2.75
    if self.value ("type_note", x, y):
      self.fd.append ("/%s %s selectfont" % self.value ("type_font", x, y))
      self.fd.append ("%s %s %s setrgbcolor"
                      % self.value ("type_text_colour", x, y))
      self.fd.append ("%d %d moveto" % (bx, by))
      self.fd.append ("(%s) show" % self.value ("type_note", x, y))

  def type_desc (self, x, y):
    bx = self.type_stripe_width - self.type_desc_inset_x - self.x_off
    by = self.type_stripe_inset_y + 2.75
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
      # Token interior
      self.fd.append ("0 setgray")
      self.fd.append ("0.3 setlinewidth")
      self.fd.append ("%d %d 15 0 360 arc" % (bx, by))
      self.fd.append ("%s %s %s setrgbcolor"
                      % self.value ("token_base_colour", x, y))
      self.fd.append ("fill")
      self.fd.append ("stroke")
      self.fd.append ("closepath")
      # Token outline
      self.fd.append ("0 setgray")
      self.fd.append ("0.3 setlinewidth")
      self.fd.append ("%d %d 15 0 360 arc" % (bx, by))
      self.fd.append ("stroke")
      self.fd.append ("closepath")
      # Top token colour
      self.fd.append ("%s %s %s setrgbcolor"
                      % self.value ("token_top_colour", x, y))
      self.fd.append ("%d %d 15 %f %f arc" % (bx, by, 0 + 15, 180 - 15))
      self.fd.append ("closepath")
      self.fd.append ("fill")
      self.fd.append ("stroke")
      # Top token outline
      self.fd.append ("0 setgray")
      self.fd.append ("0.3 setlinewidth")
      self.fd.append ("%d %d 15 %f %f arc" % (bx, by, 0 + 15, 180 - 15))
      self.fd.append ("closepath")
      self.fd.append ("stroke")
      # Bottom token colour
      self.fd.append ("%s %s %s setrgbcolor"
                      % self.value ("token_bottom_colour", x, y))
      self.fd.append ("%d %d 15 %f %f arc" % (bx, by, 180 + 15, 0 - 15))
      self.fd.append ("closepath")
      self.fd.append ("fill")
      self.fd.append ("stroke")
      # Bottom token outline
      self.fd.append ("0 setgray")
      self.fd.append ("0.3 setlinewidth")
      self.fd.append ("%d %d 15 %f %f arc" % (bx, by, 180 + 15, 0 - 15))
      self.fd.append ("closepath")
      self.fd.append ("stroke")
      # Token text
      self.fd.append ("/%s %s selectfont" % self.value ("token_font", x, y))
      self.fd.append ("0 0 0 setrgbcolor")
      self.fd.append ("%d %f moveto" % (bx, by - 10/2 + 2.5))
      self.fd.append ("(%s) dup stringwidth pop 2 div neg 0 rmoveto show"
                      % self.value ("token_name", x, y))

  def title (self, x, y):
    bx = (self.side_stripe_inset_x + self.side_stripe_width
          + self.title_inset_x
          + ((self.tile_x - self.side_stripe_inset_x
              - self.side_stripe_width - self.title_inset_x) / 2))
    by = self.tile_y - self.title_inset_y
    self.fd.append ("/%s %s selectfont" % self.value ("title_font", x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("title_colour", x, y))
    tl = self.value ("title", x, y)
    if isinstance (tl, StringType):
      tl = [tl,]
    for t in tl:
      self.fd.append ("%d %d moveto" % (bx, by))
      self.fd.append ("(%s) dup stringwidth pop 2 div neg 0 rmoveto show"
                      % t)
      by -= self.title_line_height
