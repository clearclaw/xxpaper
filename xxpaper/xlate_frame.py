#! /usr/bin/env python

from __future__ import absolute_import
import logging, logtool
from .config import Config

LOG = logging.getLogger (__name__)

class XlateFrame (object):

  @logtool.log_call
  def __init__ (self, canvas, typ, x, y, inset_by = False):
    self.canvas = canvas
    self.x_sz = Config.get (typ + "/x")
    self.y_sz = Config.get (typ + "/y")
    self.inset = Config.get (typ + "/" + inset_by) if inset_by else 0
    self.x = x
    self.y = y

  @logtool.log_call
  def __enter__ (self):
    self.canvas.saveState ()
    self.canvas.translate ((self.x * self.x_sz) + self.inset,
                           (self.y * self.y_sz) + self.inset)

  @logtool.log_call
  def __exit__ (self, etyp, e, tb):
    if etyp is None:
      self.canvas.restoreState ()
