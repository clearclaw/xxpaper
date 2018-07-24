#! /usr/bin/env python

from __future__ import absolute_import
import itertools, logging, logtool, pkg_resources
from path import Path
from reportlab.pdfgen import canvas as Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .config import Config

LOG = logging.getLogger (__name__)

class Document (object):

  @logtool.log_call
  def __init__ (self, fname, **kwargs):
    self.canvas = None
    self.fname = fname
    self.kwargs = kwargs

  @logtool.log_call
  def __enter__ (self):
    self.canvas = Canvas.Canvas (self.fname, **self.kwargs)
    ## we know some glyphs are missing, suppress warnings
    # import reportlab.rl_config
    # reportlab.rl_config.warnOnMissingFontGlyphs = 0
    for ff in Config.get ("xxpaper/typefaces", {"default": []}):
      for p in (Path (ff),
                Path (pkg_resources.resource_filename ("xxpaper", ff))):
        if p.isfile ():
          pdfmetrics.registerFont (TTFont(p.namebase, str (p)))
    return self.canvas

  @logtool.log_call
  def __exit__ (self, etyp, e, tb):
    if etyp is None:
      self.canvas.save ()
