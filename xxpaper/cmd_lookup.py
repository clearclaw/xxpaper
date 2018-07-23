#! /usr/bin/env python

from __future__ import absolute_import
import clip, logging, logtool
from .config import Config, load_config
from . import tile

LOG = logging.getLogger (__name__)
@logtool.log_call
def do (**kwargs):
  load_config (kwargs["templates"])
  components = Config.get ("DEFAULT/COMPONENTS")
  if kwargs["typ"] not in components:
    clip.exit (err = True,
               message = "Unknown object typ: %s" % kwargs["typ"])
  tl = tile.Tile (kwargs.get ("typ"),
                  None, kwargs.get ("name"),
                  kwargs.get ("n", 0))
  print "%s => %s" % (kwargs["key"], tl.value (kwargs["key"]))
