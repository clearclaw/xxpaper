#! /usr/bin/env python

from __future__ import absolute_import
import logging, logtool
from reportlab.pdfgen import canvas as Canvas

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
    return self.canvas

  @logtool.log_call
  def __exit__ (self, etyp, e, tb):
    if etyp is None:
      self.canvas.save ()
