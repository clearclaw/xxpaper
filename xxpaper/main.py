#! /usr/bin/env python

from __future__ import absolute_import
import clip, fnmatch, itertools, jinja2, logging, logtool
import os, pkg_resources, raven, re, sys
from addict import Dict
from configobj import ConfigObj
from functools import partial
from path import Path
from StringIO import StringIO
from .cmdio import CmdIO
import xxpaper
from ._version import get_versions

logging.basicConfig (level = logging.WARN)
LOG = logging.getLogger (__name__)
APP = clip.App (name = "xxpaper")
CONFIG = Dict ({
  "dump": False,
  "formats": ["outline", "nooutline",],
  "game_fname": None,
  "nocolour": False,
  "onlyone": False,
  "pages": ["*",],
  "papers": ["*",],
  "runtime": None,
  "sections": ["*",],
  "single_tiles": False,
  "template": None,
  "tile_filter": ["*",],
  "quiet": False,
})
IO = CmdIO (CONFIG)
RE_VAR = re.compile (r"\$\{([A-Za-z0-9._]+)\}")

@logtool.log_call (log_args = False)
def make (cfgs, paper, outline, section, page, fname):
  with getattr (xxpaper, section.capitalize ()) (
      cfgs, paper, outline, section, page, fname) as t:
    t.make ()

@logtool.log_call
def match_filter (name, filters):
  for f in filters:
    if fnmatch.fnmatch (name, f):
      return True
  return False

@logtool.log_call (log_args = False)
def _cfgval_exp (cfgs, section, v):
  while True:
    m = RE_VAR.search (v)
    if not m:
      break
    k = m.group (1) # Variable name
    r = get_cfgval (cfgs, section, k) # Replacement token
    if isinstance (r, basestring):
      v = "%s%s%s" % (v[:m.start(0)], r, v[m.end(0):])
    else: # Scummy, but kinda handles the tuples
      v = r
      break
  return v

@logtool.log_call (log_args = False)
def _cfgval (cfgs, section, name):
  for cfg in itertools.chain (cfgs):
    try:
      return cfg[section][name]
    except: # pylint: disable=bare-except
      pass
    try:
      return cfg["DEFAULT"][name]
    except: # pylint: disable=bare-except
      pass
  clip.exit ("Error: Cannot find the value of: %s" % name, err = True)

@logtool.log_call (log_args = False)
def get_cfgval (cfgs, section, name):
  v = _cfgval (cfgs, section, name)
  if isinstance (v, basestring):
    v = _cfgval_exp (cfgs, section, v)
  elif isinstance (v, list):
    v = [ _cfgval_exp (cfgs, section, x) for x in v]
  return v

@logtool.log_call (log_args = False, log_rc = False)
def load_configs ():
  fname = CONFIG.game_fname
  raw = fname.bytes ().decode ("unicode_escape")
  env = jinja2.Environment(extensions = ["jinja2.ext.loopcontrols",
                                         "jinja2.ext.with_",
                                         "jinja2.ext.do",])
  xxp = StringIO (env.from_string (raw).render ())
  if CONFIG.template:
    fn = Path ("./") / fname.namebase + "_expanded.cfg"
    IO.debug ("Expanded template: %s" % fn)
    with open (fn, "w") as f:
      f.write (xxp.getvalue ())
  game = ConfigObj (xxp.readlines ())
  # conf = ConfigObj (file (fname).readlines ())
  if "DEFAULT" not in game.sections:
    game["DEFAULT"] = {}
  game["DEFAULT"]["source_filename"] = "File: %s" % CONFIG.game_fname
  if CONFIG.runtime is None:
    runtime = ConfigObj (["[DEFAULT]",])
  else:
    if CONFIG.runtime.startswith ("@"):
      rtdata = pkg_resources.resource_string ("xxpaper",
                                               "%s.conf" % CONFIG.runtime[1:])
    else:
      rtdate = Path (CONFIG.verride).bytes ().decode ("unicode_escape")
    rtproc= StringIO (env.from_string (rtdata).render ())
    runtime = ConfigObj (rtproc.readlines ())
    if "DEFAULT" not in runtime.sections:
      runtime["DEFAULT"] = {}
  defdata = pkg_resources.resource_string ("xxpaper", "DEFAULT.conf")
  defproc = StringIO (env.from_string (defdata).render ())
  default = ConfigObj (defproc.readlines ())
  default["DEFAULT"]["XXP_VERSION"] = get_versions()["version"]
  return runtime, game, default

@logtool.log_call
def option_logging (flag): # pylint: disable=unused-argument
  logging.root.setLevel (logging.DEBUG)

@logtool.log_call
def option_list (option, value):
  CONFIG[option] = [s.strip () for s in value.split (",")]

@logtool.log_call
def option_setopt (option, value):
  CONFIG[option] = value

@logtool.log_call
def option_version (opt): # pylint: disable = W0613
  clip.echo (xxpaper.__version__)
  sys.exit (0)

@logtool.log_call
def arg_game_file (fname):
  fname = Path (fname)
  if not fname.isfile ():
    clip.exit ("Game file not found: %s" % fname, err = True)
  CONFIG.game_fname = fname

@APP.main (name = Path (sys.argv[0]).basename (),
           description = "18xx rapid prototyping tool")
@clip.flag ("-H", "--HELP",  help = "Help for all sub-commands")
@clip.flag ("-C", "--nocolour", name = "nocolour",
            help = "Suppress colours in reports",
            callback = partial (option_setopt, "nocolour"))
@clip.flag ("-d", "--dump", name = "dump", help = "Dump configuration stack",
            callback = partial (option_setopt, "dump"))
@clip.flag ("-D", "--debug", name = "debug", help = "Enable debug logging",
            callback = option_logging)
@clip.opt ("-f", "--formats", name = "formats",
           help = "Art formats to produce",
           callback = partial (option_list, "formats"))
@clip.opt ("-P", "--papers", name = "papers", help = "Paper sizes to produce",
           required = False, callback = partial (option_list, "papers"))
@clip.opt ("-p", "--pages", name = "pages",
           help = "Pages to produce (comma separated)",
           required = False, callback = partial (option_list, "pages"))
@clip.flag ("-q", "--quiet", name = "quiet",
            help = "Suppress information messages",
            callback = partial (option_setopt, "quiet"))
@clip.opt ("-r", "--runtime", name = "runtime",
           help = "Runtime game settings file (overrides)",
           required = False, callback = partial (option_setopt, "runtime"))
@clip.opt ("-s", "--sections", name = "sections",
           help = "Sections to produce (comma-separated)",
           required = False, callback = partial (option_list, "sections"))
@clip.flag ("-t", "--template", name = "template",
            help = "Export Jinja-expanded template file",
           required = False, callback = partial (option_setopt, "template"))
@clip.opt ("-T", "--TILE", name = "tile",
           help = "Tiles to produce (comma separated)",
           required = False, callback = partial (option_list, "tile_filter"))
@clip.flag ("-v", "--version", help = "Report installed version",
            callback = option_version)
@clip.arg (name = "game_file", nargs = 1, default = None,
           help = "XXPaper game file", required = True,
           callback = arg_game_file)
@logtool.log_call
def app_main (*args, **kwargs): # pylint: disable=unused-argument
  if not CONFIG.conf.debug:
    logging.basicConfig (level = logging.ERROR)
  if not sys.stdout.isatty ():
    option_setopt ("nocolour", True)
  runtime, game, default = load_configs ()
  cfgs = [runtime, game, default,]
  if CONFIG.dump:
    import pprint
    IO.info ("Runtime:")
    IO.report (pprint.pformat (runtime.dict ()))
    IO.info ("Game:")
    IO.report (pprint.pformat (game.dict ()))
    IO.info ("DEFAULT:")
    IO.report (pprint.pformat (default.dict ()))
    clip.exit ()
  formats = (CONFIG.formats if CONFIG.formats
              else get_cfgval (cfgs, "DEFAULT", "formats"))
  for paper in get_cfgval (cfgs, "DEFAULT", "papers"):
    if not match_filter (paper, CONFIG.papers):
      continue
    if paper.startswith ("@"):
      paper = get_cfgval (cfgs, "DEFAULT", paper[1:])
      if isinstance (paper, list):
        paper = tuple ([int (x) for x in paper])
    # IO.debug ("Paper size: %s" % paper)
    for form in formats:
      runtime["DEFAULT"]["outline"] = form
      # IO.debug ("  Format: %s" % form)
      for section in game.sections:
        if section == "DEFAULT" or not match_filter (section, CONFIG.sections):
          continue
        # IO.debug ("    Section: %s" % section)
        for page in game[section].sections:
          # IO.debug ("      Page: %s" % page)
          if not match_filter (page, CONFIG.pages):
            continue
          p_s = (paper if isinstance (paper, basestring)
                 else ("%sx%s" % (paper[0], paper[1])))
          fname_p = os.path.join ("./", "%s_%s-%s-%s"
                                % (section, page, form, p_s))
          runtime["DEFAULT"]["tile_filter"] = CONFIG.tile_filter
          # game["DEFAULT"]["this_filename"] = " This file: %s" % fname
          make (cfgs, paper, form, section, page, fname_p)

@logtool.log_call
def main ():
  try:
    APP.run ()
  except KeyboardInterrupt:
    pass
  except clip.ClipExit:
    sys.exit (0)
  except Exception as e:
    logtool.log_fault (e)
    IO.error ("Something broke!")
    client = raven.Client (
      "https://250e838eaff24eee9461682bc7160904"
      ":b455442d9dcb4773a82786844f430386@sentry.io/127918")
    h = client.captureException ()
    IO.error ("\t Sentry filed: %s" % h)
    sys.exit (1)

if __name__ == "__main__":
  main ()
