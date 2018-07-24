#! /usr/bin/env python

from __future__ import absolute_import
import itertools, logging, logtool
from reportlab.lib.units import inch
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
    x_adjust = Config.get ("xxpaper/%s_x_adjust" % typ, {"default": None})
    y_adjust = Config.get ("xxpaper/%s_y_adjust" % typ, {"default": None})
    if x_adjust is not None and y_adjust is not None:
      self.canvas.translate (x_adjust, y_adjust)
    else:
      self.canvas.translate (0.30 * inch, 0.50 * inch)
      self.canvas.setStrokeColorRGB (1, 0, 0)
      self.canvas.circle (0.75 * inch, 0, inch / 16, stroke = 1, fill = 0)
      self.canvas.circle (6.75 * inch, 0, inch / 16, stroke = 1, fill = 0)
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
