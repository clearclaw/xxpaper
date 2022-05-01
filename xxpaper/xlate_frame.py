#! /usr/bin/env python

import logging, logtool
from .config import Config

LOG = logging.getLogger (__name__)

class XlateFrame:

  @logtool.log_call
  def __init__ (self, canvas, typ, x, y, inset_by = False):
    self.canvas = canvas
    self.x_sz = Config.get (typ + "/x")
    self.y_sz = Config.get (typ + "/y")
    self.inset_x = Config.get (typ + "/" + inset_by + "_x") if inset_by else 0
    self.inset_y = Config.get (typ + "/" + inset_by + "_y") if inset_by else 0
    self.x = x
    self.y = y

  @logtool.log_call
  def __enter__ (self):
    self.canvas.saveState ()
    self.canvas.translate ((self.x * self.x_sz) + self.inset_x,
                           (self.y * self.y_sz) + self.inset_y)

  @logtool.log_call
  def __exit__ (self, etyp, e, tb):
    if etyp is None:
      self.canvas.restoreState ()
