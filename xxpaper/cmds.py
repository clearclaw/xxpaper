#! /usr/bin/env python

from __future__ import absolute_import
import clip, fnmatch, itertools, logging, logtool, os, pkg_resources
from reportlab.lib.pagesizes import letter, A4
from path import Path
from .main import app_main
from .config import Config
from . import contents, document, tile

LOG = logging.getLogger (__name__)
OPTIONS = ["help", "debug", "verbose", "version"]

@logtool.log_call
def _config_dirs (templates):
  fnames = [s.strip () for s in templates.split (",") if len (s.strip ()) != 0]
  fdirs = list (set ([Path (d).dirname () for d in fnames]))
  fdirs = ["./",] if fdirs == [] else fdirs
  cdir = Path (pkg_resources.resource_filename ("xxpaper",
                                                "XXP_DEFAULT.xxp")).dirname ()
  rc = fdirs + [cdir,]
  return rc

@logtool.log_call
def _load_config (templates):
  f_rc = Path (os.environ.get ("HOME", "./")) / ".xxpaperrc"
  if f_rc.isfile ():
    templates = ".xxpaperrc," + templates + ",XXP_DEFAULT.xxp"
  else:
    templates += ",XXP_DEFAULT.xxp"
  fnames = [s.strip () for s in templates.split (",")
                    if s.strip () != ""]
  dirs = _config_dirs (templates)
  Config (fnames = fnames, dirs = dirs)

@logtool.log_call
def _match_filter (name, filters):
  for f in filters:
    if fnmatch.fnmatch (name, f):
      return True
  return False

#
# Commands
#

@app_main.subcommand (
  name = "dump",
  description = "Dump the compiled game definition",
  inherits = OPTIONS)
@clip.arg (name = "templates", default = None,
           help = "XXPaper game files (comma separated)", required = True)
@clip.opt ("-o", "--output", name = "output", default = "yaml",
           help = "Output format", required = False)
@logtool.log_call
def dump (**kwargs):
  _load_config (kwargs["templates"])
  f = kwargs.get ("output")
  formats = (None, "JSON", "json", "YAML", "yaml", "yml", "TOML", "toml")
  if f not in formats:
    clip.exit (err = True,
               message = "Unknown format (%s), not one of: %s" % (f, formats))
  print Config.dumps (form = f)

@app_main.subcommand (
  name = "lookup",
  description = "Check the value of a key",
  inherits = OPTIONS)
@clip.arg (name = "templates",
           help = "XXPaper game files (comma separated)", required = True)
@clip.arg (name = "typ", required = True, help = "Typ to search")
@clip.arg (name = "name", required = True, help = "name to search")
@clip.arg (name = "n", required = True, help = "Number to search")
@clip.arg (name = "key",
           help = "Key to evaluate)", required = True)
@logtool.log_call
def lookup (**kwargs):
  _load_config (kwargs["templates"])
  components = Config.get ("DEFAULT/COMPONENTS")
  if kwargs["typ"] not in components:
    clip.exit (err = True,
               message = "Unknown object typ: %s" % kwargs["typ"])
  tl = tile.Tile (kwargs.get ("typ"),
                  None, kwargs.get ("name"),
                  kwargs.get ("n", 0))
  print "%s => %s" % (kwargs["key"], tl.value (kwargs["key"]))

@app_main.subcommand (
  name = "make",
  description = "Make artfile for a game",
  inherits = OPTIONS)
@clip.flag ("-c", "--cutline", name = "cutline",
            default = False, help = "Draw cutlines")
@clip.opt ("-f", "--filter", name = "filter",
           help = "Only these asset-types")
@clip.opt ("-p", "--paper", name = "paper",
           default = "A4", help = "Paper size (A4, letter)")
@clip.arg (name = "templates",
           help = "XXPaper game files (comma separated)", required = True)
@clip.arg (name = "outfile",
           help = "File to produce (default: first template .pdf)",
           required = False)
@logtool.log_call
def make (**kwargs):
  if kwargs["paper"] not in ("A4", "letter"):
    clip.exit (err = True,
               message = "Unknown paper size: %s" % kwargs["paper"])
  paper = A4 if kwargs["paper"] == "A4" else letter
  Config.set ("xxpaper/cutline", kwargs["cutline"])
  _load_config (kwargs["templates"])
  match = kwargs.get ("filter")
  if kwargs.get ("outfile") is None:
    outfile = Path (kwargs["templates"].split (",")[0]).namebase + ".pdf"
  else:
    outfile = Path (kwargs["outfile"])
  with document.Document (outfile, pagesize = paper) as canvas:
    filters = [
      "*%s*" % f for f in
      (match if match else "*").split (",")]
    components = Config.get ("DEFAULT/COMPONENTS")
    todo = itertools.chain (
      *[tile.items (canvas, c) for c in components
        if _match_filter (c, filters)]
    )
    contents.Contents (canvas, todo).render ()
