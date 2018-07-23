#! /usr/bin/env python

from __future__ import absolute_import
import clip, logging, logtool
from .config import Config, load_config

LOG = logging.getLogger (__name__)

@logtool.log_call
def do (**kwargs):
  load_config (kwargs["templates"])
  f = kwargs.get ("output")
  formats = (None, "JSON", "json", "YAML", "yaml", "yml", "TOML", "toml")
  if f not in formats:
    clip.exit (err = True,
               message = "Unknown format (%s), not one of: %s" % (f, formats))
  print Config.dumps (form = f)
