#! /usr/bin/env python

from __future__ import absolute_import
import clip, logging, logtool
from .config import Config, load_config
from . import tile

LOG = logging.getLogger (__name__)
@logtool.log_call
def do (**kwargs):
  typ = kwargs["typ"]
  name = kwargs["name"]
  n = kwargs["n"]
  key = kwargs["key"]
  load_config (kwargs["templates"])
  components = Config.get ("DEFAULT/COMPONENTS")
  if typ not in components:
    clip.exit (err = True,
               message = "Unknown object typ: %s" % typ)
  try:
    tl = tile.Tile (typ, None, name, n)
    # import pudb
    # pudb.set_trace ()
    print "%s => %s" % (key, tl.value (key))
  except: # pylint: disable=bare-except
    clip.exit (err = True, message = "Key not found.  KeyError: %s" % key)
