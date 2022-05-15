#! /usr/bin/env python

import logging, logtool, os, pkg_resources
from findfile_path import findfile_path
from path import Path
from reportlab.pdfgen import canvas as Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .config import Config

LOG = logging.getLogger (__name__)

class Document:

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
    cdir = Path (
      pkg_resources.resource_filename (
        "xxpaper",
        "XXP_DEFAULT.xxp")).dirname () # Just to get the directory
    paths = ["./", "~/.config/xxpaper", "~/.xxpaper", "~/",
             os.environ.get ("HOME", "./"), cdir] + Config._dirs
    for ff in Config.get ("xxpaper/typefaces", {"default": []}):
      p = Path (findfile_path (ff, paths))
      if p is not None:
        pdfmetrics.registerFont (
          TTFont(p.basename ().splitext ()[0], str (p)))
      else:
        raise ValueError (
          "Could not find fontfile: %s -- searched: %s" % (ff, paths))
    self.canvas.setTitle (
      "XXPaper: " + Config.get ("meta/title", {"default": "-missing-"}))
    self.canvas.setAuthor (
      Config.get ("meta/author", {"default": "-missing-"}))
    self.canvas.setSubject (
      "XXPaper: " + Config.get ("meta/subject", {"default": "-missing-"}))
    return self.canvas

  @logtool.log_call
  def __exit__ (self, etyp, e, tb):
    if etyp is None:
      self.canvas.save ()
