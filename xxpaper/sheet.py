#! /usr/bin/env python

import re, sys
from psfile import PSFile
from types import ListType

class Sheet (object):
  def __init__ (self, conf, sheet, page, fname):
    self.re_var = re.compile (r"^\$\{([A-Za-z0-9._]+)\}$")
    self.conf = conf
    self.fname = fname
    self.fd = None
    # Type of sheet
    self.sheet = sheet
    self.page = page
    self.rotate = self.value ("rotate")
    # Size of grid
    self.num_x = int (self.value ("num_across_x"))
    self.num_y = int (self.value ("num_across_y"))
    # Size of tile
    self.tile_x = int (self.value ("tile_x"))
    self.tile_y = int (self.value ("tile_y"))
    # Size of rubber frame
    self.rubber_x = int (self.value ("rubber_x"))
    self.rubber_y = int (self.value ("rubber_y"))
    # Offsets for inner tile block
    self.x_off = (self.rubber_x - (self.tile_x * 3)) / 2
    self.y_off = (self.rubber_y - (self.tile_y * 3)) / 2

  def __enter__ (self):
    return self

  def __exit__ (self, t, v, tr):
    pass

  def open (self):
    self.fd = PSFile (self.fname, paper = self.value ("paper"))
    if self.rotate == "1":
      self.fd.append ("270 rotate")
      self.fd.append ("-%d %d translate" % (self.fd.height, 0))

  def close (self):
    if self.fd:
      self.fd.close ()
      self.fd = None

  def _get_value (self, sl, k):
    base = self.conf
    al = list ()
    # Descending list of sections
    for s in sl:
      a = base.get (s)
      if not a:
        break
      al.insert (0, a)
      base = a
    al.append (self.conf.get ("DEFAULT"))
    for d in al:
      # print "K: ", k , "D: ", d, "V: [%s]" % d.get (k)
      if d.has_key (k):
        return d.get (k)
    raise ValueError

  def value (self, n, x = 0, y = 0):
    sl = [self.sheet, self.page, "tile_%d%d" % (x + 1, y + 1)]
    try:
      v = self._get_value (sl, n)
    except:
      print >> sys.stderr, (
        "FAULT: No definition found for: %s.%s.%s (%d, %d)"
        % (self.sheet, self.page, n, x + 1, y + 1))
      sys.exit (1)
    if v == "randomcolour": # Development ease
      from random import uniform
      v = (uniform (0, 1), uniform (0, 1), uniform (0, 1))
    elif isinstance (v, ListType): # So it satisfies the % operator
      v = tuple (v)
    else: # Substitute ${VAR} value
      m = self.re_var.search (v)
      if m:
        k = m.group (1) # Variable name
        v = self.value (k, x, y) # Replacement token
    return v

  def page_frame (self):
    self.fd.append ("%s %s %s setrgbcolor" % self.value ("base_colour"))
    self.fd.append ("0 0 %d %d rectfill" % (self.rubber_x, self.rubber_y))
    self.fd.append ("0 setgray")
    self.fd.append ("0.1 setlinewidth")
    self.fd.append ("0 0 %d %d rectstroke"
                    % (self.rubber_x, self.rubber_y))

  def page_tiles (self):
    ox = self.x_off
    oy = self.y_off
    for x in xrange (self.num_x):
      for y in xrange (self.num_y):
        bx = (x * self.tile_x) + ox
        by = (y * self.tile_y) + oy
        if self.value ("outline", x, y) == "1":
          self.fd.append ("0 setgray")
          self.fd.append ("0.1 setlinewidth")
          self.fd.append ("%d %d %d %d rectstroke"
                          % (bx, by, self.tile_x, self.tile_y))

  def push_tile (self, x, y):
    self.fd.append ("gsave")
    self.fd.append ("%d %d translate" % (x, y))

  def pop_tile (self):
    self.fd.append ("grestore")

  def make (self):
    self.open ()
    self.page_frame ()
    self.page_tiles ()
    self.page_details ()
    ox = self.x_off
    oy = self.y_off
    for x in xrange (self.num_x):
      for y in xrange (self.num_y):
        bx = (x * self.tile_x) + ox
        by = (y * self.tile_y) + oy
        self.push_tile (bx, by)
        self.tile_details (x, y)
        self.pop_tile ()
    self.close ()
