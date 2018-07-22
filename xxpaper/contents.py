#! /usr/bin/env python

from __future__ import absolute_import
import logging, logtool
from .page import Page
from .xlate_frame import XlateFrame

LOG = logging.getLogger (__name__)

class Contents (object):

  @logtool.log_call
  def __init__ (self, canvas, objects):
    self.canvas = canvas
    self.objects = objects

  @logtool.log_call
  def render (self):
    with Page (self.canvas) as pg:
      for obj in self.objects:
        coords = pg.next (obj.asset)
        with XlateFrame (self.canvas, obj.tile_type, *coords,
                         inset_by = "margin"):
          print "Obj: ", obj.asset
          obj.render ()
