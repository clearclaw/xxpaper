#! /usr/bin/env python

from __future__ import absolute_import
import itertools, logtool, numbers, re, sys
from psfile import PSFile
from types import ListType
from .cmdio import CmdIO

class Sheet (CmdIO):

  @logtool.log_call (log_args = False)
  def __init__ (self, cfgs, paper, outline, sheet, page, fname):
    super (Sheet, self).__init__ (cfgs)
    self.re_var = re.compile (r"\$\{([A-Za-z0-9._]+)\}")
    self.paper = paper
    self.outline = outline
    self.cfgs = cfgs
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
    self.x_off = (self.rubber_x - (self.tile_x * self.num_x)) / 2
    self.y_off = (self.rubber_y - (self.tile_y * self.num_y)) / 2

  @logtool.log_call
  def __enter__ (self):
    return self

  @logtool.log_call
  def __exit__ (self, t, v, tr):
    pass

  @logtool.log_call
  def open (self):
    self.fd = PSFile (self.fname, paper = self.paper, margin = 36)
    if self.rotate == "1":
      self.fd.append ("270 rotate")
      self.fd.append ("-%d %d translate" % (self.fd.height, 0))

  @logtool.log_call
  def close (self):
    if self.fd:
     self.fd.close ()
     self.fd = None

  @logtool.log_call (log_args = False)
  def _value_lookup (self, cfg, sl, k):
    base = cfg
    al = list ()
    # Descending list of sections
    for s in sl:
      a = base.get (s)
      if not a:
        break
      al.insert (0, a)
      base = a
    al.append (cfg.get ("DEFAULT"))
    for d in al:
      # print "K: ", k , "D: ", d, "V: [%s]" % d.get (k)
      if d.has_key (k):
        # print "Found %s / %s in %s" % (k, sl, cfg.my_name)
        return d.get (k)
    # print "Failed to find %s / %s in %s" % (k, sl, cfg.my_name)
    raise ValueError

  @logtool.log_call
  def _get_value (self, sl, k):
    for cfg in itertools.chain (self.cfgs):
      try:
        return self._value_lookup (cfg, sl, k)
      except: # pylint: disable=bare-except
        pass
    raise ValueError

  @logtool.log_call
  def value (self, n, x = 0, y = 0):
    sl = [self.sheet, self.page, "tile_%d.%d" % (x + 1, y + 1)]
    try:
      v = self._get_value (sl, n)
    except: # pylint: disable=bare-except
      print >> sys.stderr, (
        "FAULT: No definition found for: %s.%s.%s (%d, %d)"
        % (self.sheet, self.page, n, x + 1, y + 1))
      sys.exit (3)
    if v == "randomcolour": # Development ease
      from random import uniform
      v = (uniform (0, 1), uniform (0, 1), uniform (0, 1))
    elif isinstance (v, ListType): # So it satisfies the % operator
      v = tuple (v)
    else: # Substitute ${VAR} value
      while True:
        m = self.re_var.search (v)
        if not m:
          break
        k = m.group (1) # Variable name
        r = self.value (k, x, y) # Replacement token
        if isinstance (r, basestring):
          v = "%s%s%s" % (v[:m.start(0)], r, v[m.end(0):])
        else: # Scummy, but kinda handles the tuples
          v = r
          break
    return v

  @logtool.log_call
  def page_details (self):
    pass # Specialised in children

  @logtool.log_call
  def tile_details (self, x, y):
    pass # Specialised in children

  @logtool.log_call
  def tile_block (self):
    ox = self.x_off
    oy = self.y_off
    for x in xrange (self.num_x):
      for y in xrange (self.num_y):
        bx = (x * self.tile_x) + ox
        by = (y * self.tile_y) + oy
        self.push_tile (x, y, bx, by)
        self.tile_details (x, y)
        self.pop_tile ()

  @logtool.log_call
  def page_align (self):
    align_length = float (self.value ("align_length"))
    self.fd.append ("gsave")
    for i in [((self.rubber_x / 2.0, 0), (0, 0 - align_length)),
              ((self.rubber_x /2.0, self.rubber_y), (0, align_length)),
              ((0, self.rubber_y / 2.0), (0 - align_length, 0)),
              ((self.rubber_x, self.rubber_y / 2.0), (align_length, 0)),]:
      self.line ("align", 0, 0, i[0][0], i[0][1], i[1][0], i[1][1])
    self.fd.append ("grestore")

  @logtool.log_call
  def page_frame (self):
    self.box ("frame", 0, 0, 0, 0, self.rubber_x, self.rubber_y)

  @logtool.log_call
  def copyright (self):
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (0, self.rubber_y + 6))
    self.text ("copyright", 0, 0, v_centre = -1)
    self.fd.append ("grestore")
    
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (0, -12))
    self.text ("source_filename", 0, -12, v_centre = -1)
    self.fd.append ("grestore")
    
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (self.rubber_x / 2, -12))
    self.text ("this_filename", 0, -12, v_centre = -1)
    self.fd.append ("grestore")
    
    self.fd.append ("gsave")
    self.fd.append ("%f %f moveto" % (0, -24))
    self.text ("print_instruction", 0, -24, v_centre = -1)
    self.fd.append ("grestore")

  @logtool.log_call
  def push_tile (self, x, y, bx, by):
    self.fd.append ("gsave")
    self.fd.append ("%d %d translate" % (bx, by))
    if self.value ("outline", x, y) == "outline":
      self.box ("tile", x, y, 0, 0, self.tile_x, self.tile_y)
    self.fd.append ("newpath")

  @logtool.log_call
  def pop_tile (self):
    self.fd.append ("grestore")

  @logtool.log_call
  def line (self, typ, x, y, bx, by, w, h,
            dash_length = None, dash_space = 5, dash_start = 0):
    stroke_width = float (self.value ("%s_stroke" % typ, x, y))
    colour = self.value ("%s_colour" % typ, x, y)
    if colour != "transparent":
      self.fd.append ("gsave")
      if isinstance (dash_length, numbers.Number):
        self.fd.append ("1 setlinecap")
        self.fd.append ("[%s %s] %s setdash" % (dash_length, dash_space, dash_start))
      self.fd.append ("%s %s %s setrgbcolor" % colour)
      self.fd.append ("%f setlinewidth" % stroke_width)
      self.fd.append ("%f %f moveto" % (bx, by))
      self.fd.append ("%f %f lineto" % (bx + w, by + h))
      self.fd.append ("stroke")
      self.fd.append ("grestore")

  @logtool.log_call
  def box (self, typ, x, y, bx, by, w, h):
    stroke = float (self.value ("%s_stroke" % typ, x, y))
    stroke_colour = self.value ("%s_stroke_colour" % typ, x, y)
    colour_bg = self.value ("%s_colour" % typ, x, y)
    self.fd.append ("gsave")
    if colour_bg != "transparent":
      self.fd.append ("%s %s %s setrgbcolor" % colour_bg)
      self.fd.append ("%f %f %f %f rectfill" % (bx, by, w, h))
    if stroke_colour != "transparent":
      self.fd.append ("%s %s %s setrgbcolor" % stroke_colour)
      self.fd.append ("%f setlinewidth" % stroke)
      self.fd.append ("%f %f %f %f rectstroke" % (bx, by, w, h))
    self.fd.append ("grestore")

  @logtool.log_call
  def text (self, typ, x, y, h_centre = -1, v_centre = 1):
    line_height = float (self.value ("%s_line_height" % typ))
    self.fd.append ("gsave")
    self.fd.append ("currentpoint translate")
    self.fd.append ("/%s %s selectfont" % self.value ("%s_font" % typ, x, y))
    self.fd.append ("%s %s %s setrgbcolor"
                    % self.value ("%s_colour" % typ, x, y))
    tl = self.value (typ, x, y)
    if isinstance (tl, basestring):
      tl = tl.split ("\n") # pylint: disable=no-member
    if v_centre == 1:
      by = 0
    if v_centre == 0:
      by = line_height * ((float (len (tl) - 1) / 2))
      self.fd.append ("0 %d moveto" % by)
    if v_centre == -1:
      by = line_height * (len (tl) - 1)
      self.fd.append ("0 %d moveto" % by)
    tformat = {
      -1: "(%s) show",
      0: "(%s) dup stringwidth pop 2 div neg 0 rmoveto show",
      1: "(%s) dup stringwidth pop neg 0 rmoveto show",
      }
    for t in tl:
      self.fd.append (tformat[h_centre] % t)
      by -= line_height
      self.fd.append ("0 %d moveto" % by)
    self.fd.append ("grestore")

  @logtool.log_call
  def company_token_circle (self, x, y):
    token_radius = float (self.value ("token_radius", x, y))
    colour = self.value ("token_colour", x, y)
    stroke = float (self.value ("token_stroke", x, y))
    stroke_colour = self.value ("token_stroke_colour", x, y)
    ps = """
      gsave
      currentpoint translate
      newpath
      0 0 {token_radius} 0 360 arc
      gsave
      {colour} setrgbcolor
      fill
      grestore
      {stroke_colour} setrgbcolor
      {stroke} setlinewidth
      stroke
      grestore
    """.format (**{
      "token_radius": token_radius,
      "colour": "%s %s %s" % colour,
      "stroke_colour": "%s %s %s" % stroke_colour,
      "stroke": stroke,
    })
    self.fd.append (ps)

  @logtool.log_call
  def company_token (self, x, y):
    stroke = float (self.value ("token_stroke", x, y))
    stroke_colour = self.value ("token_stroke_colour", x, y)
    radius = float (self.value ("token_radius", x, y))
    stripe_angle = float (self.value ("token_stripe_angle", x, y))
    top_colour = self.value ("token_top_colour", x, y)
    top_stripe_colour = self.value ("token_top_stripe_colour", x, y)
    bottom_colour = self.value ("token_bottom_colour", x, y)
    bottom_stripe_colour = self.value ("token_bottom_stripe_colour", x, y)
    stripe_text_fudge = float (self.value ("token_stripe_text_fudge", x, y))
    self.company_token_circle (x, y)
    # Setup
    self.fd.append ("gsave")
    self.fd.append ("currentpoint translate")
    self.fd.append ("newpath")
    # Token top
    self.fd.append ("gsave")
    self.fd.append ("0 0 %f %f %f arc"
                    % (radius, 0 + stripe_angle, 180 - stripe_angle))
    self.fd.append ("closepath")
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor" % top_colour)
    self.fd.append ("fill")
    self.fd.append ("grestore")
    self.fd.append ("%s %s %s setrgbcolor" % stroke_colour)
    self.fd.append ("%f setlinewidth" % stroke)
    self.fd.append ("stroke")
    self.fd.append ("grestore")
    # Token top stripe
    if top_stripe_colour != "transparent":
      angle1 = float (self.value ("token_top_stripe_angle1", x, y))
      angle2 = float (self.value ("token_top_stripe_angle2", x, y))
      self.fd.append ("gsave")
      self.fd.append ("0 0 %f %f %f arc"
                      % (radius, 0 + angle1, 0 + angle2))
      self.fd.append ("0 0 %f %f %f arc"
                      % (radius, 180 - angle2, 180 - angle1))
      self.fd.append ("closepath")
      self.fd.append ("gsave")
      self.fd.append ("%s %s %s setrgbcolor" % top_stripe_colour)
      self.fd.append ("fill")
      self.fd.append ("grestore")
      self.fd.append ("%s %s %s setrgbcolor" % stroke_colour)
      self.fd.append ("%f setlinewidth" % stroke)
      self.fd.append ("stroke")
      self.fd.append ("grestore")
    # Token bottom
    self.fd.append ("gsave")
    self.fd.append ("0 0 %f %f %f arc"
                    % (radius, 180 + stripe_angle, 0 - stripe_angle))
    self.fd.append ("closepath")
    self.fd.append ("gsave")
    self.fd.append ("%s %s %s setrgbcolor" % bottom_colour)
    self.fd.append ("fill")
    self.fd.append ("grestore")
    self.fd.append ("%s %s %s setrgbcolor" % stroke_colour)
    self.fd.append ("%f setlinewidth" % stroke)
    self.fd.append ("stroke")
    self.fd.append ("grestore")
    # Token bottom stripe
    if bottom_stripe_colour != "transparent":
      angle1 = float (self.value ("token_bottom_stripe_angle1", x, y))
      angle2 = float (self.value ("token_bottom_stripe_angle2", x, y))
      self.fd.append ("gsave")
      self.fd.append ("0 0 %f %f %f arc"
                      % (radius, 180 + angle1, 180 + angle2))
      self.fd.append ("0 0 %f %f %f arc"
                      % (radius, 0 - angle2, 0 - angle1))
      self.fd.append ("closepath")
      self.fd.append ("gsave")
      self.fd.append ("%s %s %s setrgbcolor" % bottom_stripe_colour)
      self.fd.append ("fill")
      self.fd.append ("grestore")
      self.fd.append ("%s %s %s setrgbcolor" % stroke_colour)
      self.fd.append ("%f setlinewidth" % stroke)
      self.fd.append ("stroke")
      self.fd.append ("grestore")
    # Token text
    self.fd.append ("gsave")
    self.fd.append ("0 %f moveto" % (0 - stripe_text_fudge))
    self.text ("token_name", x, y, h_centre = 0, v_centre = 0)
    self.fd.append ("grestore")
    # Done
    self.fd.append ("grestore")

  def make (self):
    self.open ()
    self.page_align ()
    self.page_frame ()
    self.page_details ()
    self.tile_block ()
    self.copyright ()
    self.close ()
