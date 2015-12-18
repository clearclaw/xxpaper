#!/usr/bin/env python

import clip, logtool, termcolor
from addict import Dict

COLOUR_ERROR = "red"
COLOUR_DEBUG = "blue"
COLOUR_INFO = "white"
COLOUR_INFO_BAD = "magenta"
COLOUR_WARN = "yellow"
COLOUR_REPORT = "green"
COLOUR_FIELDNAME = "cyan"
COLOUR_VALUE = "green"

class CmdIO (object):

  @logtool.log_call
  def __init__ (self, *args, **kwargs): # pylint: disable = W0613
    self.conf = Dict ()

  @logtool.log_call
  def colourise (self, msg, colour):
    return (termcolor.colored (msg, colour) if not self.conf.nocolour
            else msg)

  @logtool.log_call
  def debug (self, msg):
    if not self.conf.quiet:
      clip.echo (self.colourise (msg, COLOUR_DEBUG))

  @logtool.log_call
  def info (self, msg, err = False):
    if not self.conf.quiet:
      clip.echo (self.colourise (msg,
                                 COLOUR_INFO if not err else COLOUR_INFO_BAD))

  @logtool.log_call
  def error (self, msg):
    if not self.conf.quiet:
      clip.echo (self.colourise (msg, COLOUR_ERROR))

  @logtool.log_call
  def warn (self, msg):
    if not self.conf.quiet:
      clip.echo (self.colourise ("WARNING: " + msg, COLOUR_WARN))

  @logtool.log_call
  def report (self, msg, err = False):
    if not self.conf.quiet:
      clip.echo (self.colourise (msg, COLOUR_REPORT if not err
                                 else COLOUR_ERROR))

  @logtool.log_call
  def report_field (self, field, value, err = False):
    if not self.conf.quiet:
      clip.echo ("%s: %s" % (
        self.colourise (field, COLOUR_FIELDNAME),
        self.colourise (value,
                        COLOUR_VALUE if not err else COLOUR_ERROR),))
