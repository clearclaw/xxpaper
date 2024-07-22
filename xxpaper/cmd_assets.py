#! /usr/bin/env python

import clip, fnmatch, itertools, logging, logtool
from reportlab.lib.pagesizes import letter, A4
from path import Path
from .config import Config, load_config
from . import contents, document, tile

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
  if kwargs["paper"] not in ("A4", "letter"):
    clip.exit (err = True,
               message = "Unknown paper size: %s" % kwargs["paper"])
  paper = A4 if kwargs["paper"] == "A4" else letter
  Config.set ("xxpaper/cutline", kwargs["cutline"])
  load_config (kwargs["templates"])
  nam_match = kwargs.get ("name")
  typ_match = kwargs.get ("filter")
  if kwargs.get ("outfile") is None:
    outfile = Path (
      kwargs["templates"].split (",")[0]).basename ().splitext ()[0] + ".pdf"
  else:
    outfile = Path (kwargs["outfile"])
  with document.Document (outfile, pagesize = paper) as canvas:
    nam_filters = [
      "%s*" % f for f in
      (nam_match if nam_match else "*").split (",")]
    typ_filters = [
      "*%s*" % f for f in
      (typ_match if typ_match else "*").split (",")]
    repeats = [s.strip () for s in kwargs["repeat"].split (",")]
    components = Config.get ("DEFAULT/COMPONENTS")
    todo = itertools.chain (
      *[[n for n in tile.items (canvas, c)
         if _match_filter (n.name, nam_filters)]
        * (repeats.count (c) + 1)
        for c in components
        if _match_filter (c, typ_filters)]
    )
    contents.Contents (canvas, todo).render ()
