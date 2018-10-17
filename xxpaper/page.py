#! /usr/bin/env python

from __future__ import absolute_import
import itertools, logging, logtool, sys
from reportlab.lib.units import inch
from path import Path
from . import __version__
from .config import Config
from .tile import Tile
from .xlate_frame import XlateFrame

LOG = logging.getLogger (__name__)

class Page (object):

  @logtool.log_call
  def __init__ (self, canvas):
    self.canvas = canvas
    self.asset = None
    self.in_page = False
    self.line = None
    self.x_dim = None
    self.y_dim = None
    self.ndx = 0

  @logtool.log_call
  def _borders (self):
    if (Config.get ("xxpaper/cutline", {"default": False})
        and self.asset is not None):
      for x, y in itertools.product (range (self.x_dim), range (self.y_dim)):
        with XlateFrame (self.canvas,
                         Config.get ("CATALOGUE/" + self.asset)["tile_type"],
                         x, y):
          Tile (self.asset, self.canvas, None, 0).cutline ()

  @logtool.log_call
  def _end_page (self):
    if self.asset is not None:
      print "EndPage"
      self._borders ()
      self.canvas.restoreState ()
      self.canvas.showPage ()
      self.in_page = False

  @logtool.log_call
  def _start_page (self, asset, typ):
    if self.in_page:
      self._end_page ()
    print "StartPage"
    self.canvas.saveState ()
    x_adjust = Config.get ("user/%s_x_adjust" % typ, {"default": None})
    y_adjust = Config.get ("user/%s_y_adjust" % typ, {"default": None})
    nomark = Config.get ("DEFAULT/no_registration", {"default": []})
    print "============", x_adjust, y_adjust, nomark, typ
    if typ in nomark and x_adjust is not None and y_adjust is not None:
      self.canvas.saveState ()
      self.canvas.setStrokeColorRGB (0, 0, 0)
      self.canvas.setLineWidth (0.2)
      self.canvas.circle (0, 0,
                          0.15 * inch / 2.0,
                          stroke = 1, fill = 0)
      self.canvas.line (0, 0, 0, 36)
      self.canvas.line (0, 0, 36, 0)
      self.canvas.restoreState ()
      self.canvas.translate (x_adjust, y_adjust)
      self.canvas.saveState ()
      self.canvas.setStrokeColorRGB (0, 0, 0)
      self.canvas.setLineWidth (0.2)
      self.canvas.setFillColorRGB (0, 0, 0)
      self.canvas.circle (0, 0,
                          0.15 * inch / 2.0,
                          stroke = 1, fill = 1)
      self.canvas.line (0, 0, 0, 36)
      self.canvas.line (0, 0, 36, 0)
      self.canvas.restoreState ()
    else:
      self.canvas.translate (0.30 * inch, 0.30 * inch)
      self.canvas.saveState ()
      self.canvas.setStrokeColorRGB (0, 0, 0)
      self.canvas.setLineWidth (0.2)
      self.canvas.circle (0.75 * inch, 0,
                          0.18 * inch / 2.0,
                          stroke = 1, fill = 0)
      self.canvas.circle (6.75 * inch, 0,
                          0.18 * inch / 2.0,
                          stroke = 1, fill = 0)
      self.canvas.setFillColorRGB (0, 0, 0)
      self.canvas.circle (0.75 * inch, 0,
                          0.1253 * inch / 2.0,
                          stroke = 0, fill = 1)
      self.canvas.circle (6.75 * inch, 0,
                          0.1253 * inch / 2.0,
                          stroke = 0, fill = 1)
      self.canvas.setFillColorRGB (0, 0, 0)
      self.canvas.setFont ("Times-Roman", 10)
      self.canvas.drawCentredString (
        (6 * inch) / 2.0 + 0.75 * inch, 4,
        "XXPaper run: " + (
          " ".join ([str (Path (sys.argv[0]).namebase),] + sys.argv[1:])))
      self.canvas.drawCentredString ((6 * inch) / 2.0 + 0.75 * inch, -8,
                                     "XXPaper version: %s" % __version__)
      self.canvas.restoreState ()
      self.canvas.translate (0, 0.25 * inch)
    self.x_dim = Config.get (typ + "/x_num")
    self.y_dim = Config.get (typ + "/y_num")
    self.line = itertools.product (xrange (self.x_dim), xrange (self.y_dim))
    self.asset = asset
    self.ndx = 0
    self.in_page = True

  @logtool.log_call
  def next (self, asset):
    old_typ = (Config.get ("CATALOGUE/" + self.asset)["tile_type"]
               if self.asset is not None else None)
    new_typ = Config.get ("CATALOGUE/" + asset)["tile_type"]
    if old_typ != new_typ:
      self._start_page (asset, new_typ)
    self.ndx += 1
    try:
      return self.line.next ()
    except StopIteration:
      self._end_page ()
      self._start_page (asset, new_typ)
      self.line = itertools.product (xrange (self.x_dim), xrange (self.y_dim))
      return self.line.next ()

  @logtool.log_call
  def __enter__ (self):
    #self.canvas.saveState ()
    return self

  @logtool.log_call
  def __exit__ (self, etyp, e, tb):
    if etyp is None:
      self._end_page ()
