#! /usr/bin/env python

import fnmatch, itertools, logging, logtool
from .config import Config, load_config
from . import cards, tile

LOG = logging.getLogger (__name__)
OPTIONS = ["help", "debug", "verbose", "version"]

@logtool.log_call
def _match_filter (name, filters):
  for f in filters:
    if fnmatch.fnmatch (name, f):
      return True
  return False

@logtool.log_call
def do (**kwargs):
  # Config.set ("xxpaper/cutline", kwargs["cutline"])
  load_config (kwargs["templates"])
  match = kwargs.get ("filter")
  filters = [
    "*%s*" % f for f in
    (match if match else "*").split (",")]
  components = Config.get ("DEFAULT/COMPONENTS")
  todo = itertools.chain (
    *[tile.items (None, c)
      for c in components
      if _match_filter (c, filters)]
  )
  cards.Cards (todo).render (kwargs)
