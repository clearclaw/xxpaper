#! /usr/bin/env python

from __future__ import absolute_import
import colorsys, itertools, json, logging, logtool, os, pkg_resources
import pprint, re, toml, yaml, math
from path import Path
from cfgstack import CfgStack
from . import __version__

LOG = logging.getLogger (__name__)
QUERIES = [
  "{klass}/index/{name}/{typ}/index/{n}/_/{obj}_{key}",
  "{klass}/index/{name}/{typ}/index/{n}/{obj}/{key}",
  "{klass}/index/{name}/{typ}/_/{obj}_{key}",
  "{klass}/index/{name}/{typ}/{obj}/{key}",
  "{klass}/index/{name}/_/{obj}_{key}",
  "{klass}/index/{name}/{obj}/{key}",
  "{klass}/{typ}/index/{n}/_/{obj}_{key}",
  "{klass}/{typ}/index/{n}/{obj}/{key}",
  "{klass}/{typ}/_/{obj}_{key}",
  "{klass}/{typ}/{obj}/{key}",
  "{klass}/index/{n}/_/{obj}_{key}",
  "{klass}/index/{n}/{obj}/{key}",
  "{klass}/_/{obj}_{key}",
  "{klass}/{obj}/{key}",
  "user/{obj}/{key}",
  "xxpaper/{obj}/{key}",
  "DEFAULT/{obj}/{key}",
  "DEFAULT/{key}",
  #"{original}",
]
RE_VAR = re.compile (r"(\$\{([A-Za-z0-9_-]*/)*([A-Za-z0-9_.-]*)\})")
EXP_VAR = re.compile (r"(\$\[[^\]]*\])")

#
# Helper functions for game files
#

@logtool.log_call
def index_of (n):
  return {"%s" % i: None for i in xrange (n)}

@logtool.log_call
def desaturate_and_brighten (colour, s, b):
  hsv_colour = colorsys.rgb_to_hsv(*colour)
  desaturated_hsv_colour = (hsv_colour[0],
                            hsv_colour[1] * s,
                            hsv_colour[1] + (1 - hsv_colour[1]) * b)
  desaturated_rgb_colour = colorsys.hsv_to_rgb (*desaturated_hsv_colour)
  return list (desaturated_rgb_colour)

@logtool.log_call
def black_or_white (colour):
  brightness = math.sqrt (colour[0] ** 2 * 0.299
                          + colour[1] ** 2 * 0.587
                          + colour[2] ** 2 * 0.114)
  return "${colour/xxp/" + ("BLACK}" if brightness > 0.6 else "WHITE}")

#
# Config
#

class Config (object):
  _state = {}
  _verbose = False

  @logtool.log_call
  @classmethod
  def __init__ (cls, fnames = None, dirs = None):
    if fnames is not None:
      exts = ("", ".xxp", ".json", ".yaml", ".yml", ".toml")
      cls._state.update (CfgStack (
        fnames, dirs = dirs, exts = exts).data.to_dict ())

  #@logtool.log_call
  @classmethod
  def _get (cls, key, params):
    # pylint: disable=too-many-branches
    rc = cls._state
    for k in key.split ("/"):
      if k == ".":
        return rc # Breaks the descent!
      rc = rc[k]
      if isinstance (rc, basestring):
        rc = rc.strip ()
      changed = True
      while changed:
        changed = False
        while isinstance (rc, basestring):
          m = RE_VAR.search (rc)
          if m is None:
            break
          if cls._verbose:
            print "    Interpolation: %s" % rc[m.start ():m.end ()]
          v = cls.get (rc[m.start () + 2:m.end () - 1], params = params)
          if isinstance (v, basestring):
            v = v.strip ()
          if m.end () - m.start () == len (rc):
            rc = v
          else:
            if isinstance (v, list): # Get rid of squares
              v = tuple (v)
            rc = ("%s%s%s" % (rc[:m.start ()], v, rc[m.end ():])).strip ()
          changed = True
          continue
        while isinstance (rc, basestring):
          m = EXP_VAR.search (rc)
          if m is not None:
            # pylint: disable=eval-used
            l = {
              "black_or_white": black_or_white,
              "desaturate_and_brighten": desaturate_and_brighten,
              "index_of": index_of,
            }
            l.update (params if params else {})
            v = eval (rc[m.start () + 2:m.end () - 1], {}, l)
            if cls._verbose:
              print "    Expression: %s => %s" % (rc[m.start ():m.end ()], v)
            if m.end () - m.start () == len (rc):
              rc = v
            else:
              rc = ("%s%s%s" % (rc[:m.start ()], v, rc[m.end ():])).strip ()
            changed = True
            continue
          break
    return rc

  #@logtool.log_call
  @classmethod
  def get (cls, key, params = None):
    if key.startswith ("colour/"): # This is a grody hack
      key = key[7:]
      if params:
        p = {}
        p.update (params)
        p["klass"] = "colour"
        params = p
    if cls._verbose:
      print "  %s =>" % key
    o, k = key.split ("/")
    for q in itertools.chain (QUERIES, [key,]):
      try:
        key_exp = q.format (obj = o, key = k, **(params if params else {}))
        if cls._verbose:
          print "    %s =>" % key_exp
        rc = cls._get (key_exp, params)
        if cls._verbose:
          print "  %s\n" % rc
        return rc
      except (AttributeError, KeyError, TypeError):
        continue
    if params and "default" in params:
      if cls._verbose:
        print "  %s => %s\n    %s\n" % (key, "(default)", params["default"])
      return params["default"]
    raise KeyError ("Not found: " + key)

  @logtool.log_call
  @classmethod
  def set (cls, key, value):
    keys = [cls._state,] + key.split ("/")
    l = keys[:-1]
    r = keys[-1]
    reduce (lambda x, y: x[y], l)[r] = value

  @classmethod
  @logtool.log_call
  def as_json (cls, indent = 2):
    return json.dumps (cls._state, indent = indent)

  @classmethod
  @logtool.log_call
  def as_yaml (cls, indent = 2):
    return yaml.dump (cls._state, width = 70, indent = indent,
                      default_flow_style = False)

  @classmethod
  @logtool.log_call
  def as_toml (cls):
    return toml.dumps (cls._state)

  @classmethod
  @logtool.log_call
  def as_pretty (cls):
    return pprint.pformat (cls._state)

  @classmethod
  @logtool.log_call
  def dumps (cls, form = "yaml", indent = 2):
    if form is None:
      form = "yaml"
    if form in ("JSON", "json"):
      return cls.as_json (indent = indent)
    elif form in ("YAML", "yaml", "yml"):
      return cls.as_yaml (indent = indent)
    elif form in ("TOML", "toml"):
      return cls.as_toml ()
    else:
      raise ValueError ("Unknown form: " + form)

#
# Loaders
#

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
def load_config (templates):
  f_rc = Path (os.environ.get ("HOME", "./")) / ".xxpaperrc"
  if f_rc.isfile ():
    templates = str (f_rc) + "," + templates + ",XXP_DEFAULT.xxp"
  else:
    templates += ",XXP_DEFAULT.xxp"
  fnames = [s.strip () for s in templates.split (",")
                    if s.strip () != ""]
  dirs = _config_dirs (templates)
  Config (fnames = fnames, dirs = dirs)
  Config.set ("xxpaper/version", __version__)
