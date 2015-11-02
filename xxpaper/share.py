#! /usr/bin/env python

from xxpaper.sheet import Sheet

class Share (Sheet):
  def __init__ (self, cfgs, sheet, page, fname):
    Sheet.__init__ (self, cfgs, sheet, page, fname)
    # Offsets within tile
    self.side_stripe_inset_x = float (self.value ("side_stripe_inset_x"))
    self.side_stripe_width = float (self.value ("side_stripe_width"))
    self.type_stripe_height = float (self.value ("type_stripe_height"))
    self.type_stripe_inset_x = float (self.value ("type_stripe_inset_x"))
    self.type_stripe_inset_y = float (self.value ("type_stripe_inset_y"))
    self.type_stripe_inset_y_fudge = float (
      self.value ("type_stripe_inset_y_fudge"))
    self.type_stripe_width = (self.x_off + self.tile_x -
                              self.type_stripe_inset_x)
    self.side_split_count = int (self.value ("side_split_count"))
    self.side_split_width = float (self.value ("side_split_width"))

  def page_details (self):
    self.side_stripe ()
    self.side_stripe_split ()
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
      self.box ("stripe", 0, 0, bx, 0, self.side_stripe_width, self.rubber_y)

  def side_stripe_split (self):
    gap = self.side_stripe_width / (self.side_split_count + 1)
    ox = self.x_off + self.side_stripe_inset_x - (self.side_split_width / 2)
    for x in xrange (self.num_x):
      for i in xrange (self.side_split_count):
        bx = (self.tile_x * x) + ox + ((i + 1) * gap)
        self.box ("side_split", 0, 0, bx, 0,
                  self.side_split_width, self.rubber_y)

  def type_stripe (self):
    oy = self.y_off + self.type_stripe_inset_y
    for y in xrange (self.num_y):
      by = (y * self.tile_y) + oy
      self.box ("type", 0, y, 0, by,
                self.type_stripe_width, self.type_stripe_height)

  def type_size (self, x, y):
    type_colour = self.value ("type_colour", x, y)
    if type_colour == "transparent":
      bx = self.side_stripe_inset_x
      by = self.type_stripe_inset_y
      self.box ("size_box", x, y, bx, by,
                self.side_stripe_width, self.type_stripe_height)
    bx = self.side_stripe_inset_x + (self.side_stripe_width / 2)
    by = self.type_stripe_inset_y + self.type_stripe_inset_y_fudge
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("size", x, y, h_centre = 0, v_centre = 1)

  def type_note (self, x, y):
    inset_x = float (self.value ("type_note_inset_x"))
    bx = (self.side_stripe_inset_x + self.side_stripe_width + inset_x)
    by = self.type_stripe_inset_y + self.type_stripe_inset_y_fudge
    if self.value ("note", x, y):
      self.fd.append ("%f %f moveto" % (bx, by))
      self.text ("note", x, y, h_centre = -1, v_centre = 1)

  def type_desc (self, x, y):
    inset_x = float (self.value ("type_desc_inset_x"))
    bx = self.type_stripe_width - inset_x - self.x_off
    by = self.type_stripe_inset_y + self.type_stripe_inset_y_fudge
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("desc", x, y, h_centre = 1, v_centre = 1)

  def tokens (self, x, y):
    inset_y = float (self.value ("token_inset_y"))
    ox = self.side_stripe_inset_x + (self.side_stripe_width / 2)
    oy = (self.type_stripe_inset_y + self.type_stripe_height + inset_y)
    gap = self.tile_y - oy - inset_y
    count = int (self.value ("token_count", x, y))
    spacing = gap / (count + 1)
    for i in xrange (1, count + 1):
      bx = ox
      by = oy + (i * spacing)
      self.fd.append ("%f %f moveto" % (bx, by))
      self.company_token (x, y)

  def title (self, x, y):
    inset_x = float (self.value ("title_inset_x"))
    inset_y = float (self.value ("title_inset_y"))
    o = (self.side_stripe_inset_x + self.side_stripe_width + inset_x)
    w = self.tile_x - o
    bx = (o + (w / 2))
    by = self.tile_y - inset_y
    self.fd.append ("%f %f moveto" % (bx, by))
    self.text ("title", x, y, h_centre = 0, v_centre = 1)
