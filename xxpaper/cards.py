#! /usr/bin/env python

import logging, logtool
from path import Path
from .config import Config
from .xlate_frame import XlateFrame
from . import document

LOG = logging.getLogger (__name__)

class Cards:

  @logtool.log_call
  def __init__ (self, objects):
    self.objects = objects

  @logtool.log_call
  def render (self, kwargs):
    for obj in self.objects:
      if kwargs.get ("outfile") is None:
        outfile = (Path (
          kwargs["templates"].split (",")[0]).basename ().splitext ()[0]
                   + "--%s_%s_%s.pdf" % (obj.name, obj.asset, obj.n))
      else:
        outfile = Path (kwargs["outfile"]
                        + "--%s_%s_%s.pdf" % (obj.name, obj.asset, obj.n))
      catalogue = Config.get ("CATALOGUE/" + obj.asset)
      tile_type = catalogue["tile_type"]
      x = Config.get (tile_type + "/x")
      y = Config.get (tile_type + "/y")
      Config.set ("xxpaper/tile_type", tile_type)
      with document.Document (
          outfile, pagesize = (float (x), float (y))) as canvas:
        obj.canvas = canvas
        canvas.saveState ()
        with XlateFrame (canvas, obj.tile_type, 0, 0,
                         inset_by = "inset"):
          obj.render ()
        canvas.restoreState ()
