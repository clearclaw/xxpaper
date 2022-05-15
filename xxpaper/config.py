#! /usr/bin/env python

import colorsys, functools, itertools, json, logging, logtool
import os, pkg_resources
import pprint, re, toml, yaml, math
from cfgstack import CfgStack
from findfile_path import findfile_path
from path import Path
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
  return {"%s" % i: None for i in range (n)}

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

class Config:
  _dirs = None
  _exts = ("", ".xxp", ".json", ".yaml", ".yml", ".toml")
  _fnames = None
  _state = {}
  _templates = None
  _verbose = False

  @logtool.log_call
  @classmethod
  def __init__ (cls, templates = None):
    if templates is not None:
      cls.templates = templates
      cls._get_conffiles ()
      # pylint: disable=not-an-iterable()
      cls._dirs = list ({Path (d).dirname () for d in cls._fnames
         if Path (d).dirname () != ""})
      # dirs -- In case there are nested _includes_s
      cls._state.update (CfgStack (
        cls._fnames, dirs = cls._dirs, exts = cls._exts).data.to_dict ())

  @logtool.log_call
  @classmethod
  def _get_conffiles (cls):
    cdir = Path (
      pkg_resources.resource_filename (
        "xxpaper",
        "XXP_DEFAULT.xxp")).dirname ()
    paths = ["./", "~/.config/xxpaper", "~/.xxpaper", "~/",
             os.environ.get ("HOME", "./"), cdir]
    rcfile = findfile_path (("xxpaperrc", ".xxpaperrc"), paths, cls._exts)
    cls._fnames = [rcfile] if rcfile is not None else []
    for t in cls.templates.split(","):
      if t.strip () == "":
        continue
      p = Path (t).dirname () if Path (t).dirname () != "" else "./"
      tfile = findfile_path (t, [p,] + paths, cls._exts)
      if tfile is None:
        # Must find the files the user specifies
        raise ValueError ("Could not find file for parameter: %s" % t)
      cls._fnames.append (tfile)
    cfile = findfile_path ("XXP_DEFAULT", paths, cls._exts)
    if cfile is not None:
      cls._fnames.append (cfile)

  @logtool.log_call
  @classmethod
  def _expand_str (cls, s, params):
    # pylint: disable=too-many-branches
    if not isinstance (s, str):
      return s
    rc = s.strip ()
    changed = True
    while changed:
      changed = False
      while isinstance (rc, str):
        m = RE_VAR.search (rc)
        if m is None:
          break
        if cls._verbose:
          print ("    Interpolation: %s" % rc[m.start ():m.end ()])
        v = cls.get (rc[m.start () + 2:m.end () - 1], params = params)
        if isinstance (v, str):
          v = v.strip ()
        if m.end () - m.start () == len (rc):
          rc = v
        else:
          if isinstance (v, list): # Get rid of squares
            v = tuple (v)
          rc = ("%s%s%s" % (rc[:m.start ()], v, rc[m.end ():])).strip ()
        changed = True
        continue
      while isinstance (rc, str):
        m = EXP_VAR.search (rc)
        if m is not None:
          # pylint: disable=eval-used
          l = {
            "black_or_white": black_or_white,
            "desaturate_and_brighten": desaturate_and_brighten,
            "index_of": index_of,
            "math": math,
          }
          l.update (params if params else {})
          v = eval (rc[m.start () + 2:m.end () - 1], {}, l)
          if cls._verbose:
            print ("    Expression: %s => %s" % (rc[m.start ():m.end ()], v))
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
  def _expand_vector (cls, v, params):
    if isinstance (v, (list, tuple)):
      return [cls._expand (i, params) for i in v]
    return v

  #@logtool.log_call
  @classmethod
  def _expand (cls, v, params):
    if isinstance (v, (list, tuple)):
      return cls._expand_vector (v, params)
    if isinstance (v, str):
      return cls._expand_str (v, params)
    return v

  #@logtool.log_call
  @classmethod
  def expand (cls, v, params = None):
    if cls._verbose:
      print ("  %s =>" % v)
    rc = cls._expand (v, params)
    if cls._verbose:
      print ("  %s\n" % rc)
    return rc

  #@logtool.log_call
  @classmethod
  def _get (cls, key, params):
    # pylint: disable=too-many-branches
    rc = cls._state
    for k in key.split ("/"):
      if k == ".":
        return rc # Breaks the descent!
      rc = rc[k]
      rc = cls._expand (rc, params)
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
      print ("  %s =>" % key)
    o, k = key.split ("/")
    for q in itertools.chain (QUERIES, [key,]):
      try:
        key_exp = q.format (obj = o, key = k, **(params if params else {}))
        if cls._verbose:
          print ("    %s =>" % key_exp)
        rc = cls._get (key_exp, params)
        if cls._verbose:
          print ("  %s\n" % rc)
        return cls.expand (rc, params)
      except (AttributeError, KeyError, TypeError):
        continue
    if params and "default" in params:
      if cls._verbose:
        print ("  %s => %s\n    %s\n" % (key, "(default)", params["default"]))
      return cls.expand (params["default"], params)
    raise KeyError ("Not found: " + key)

  @logtool.log_call
  @classmethod
  def set (cls, key, value):
    keys = [cls._state,] + key.split ("/")
    l = keys[:-1]
    r = keys[-1]
    functools.reduce (lambda x, y: x[y], l)[r] = value

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
    if form in ("YAML", "yaml", "yml"):
      return cls.as_yaml (indent = indent)
    if form in ("TOML", "toml"):
      return cls.as_toml ()
    raise ValueError ("Unknown form: " + form)

#
# Loaders
#

@logtool.log_call
def load_config (templates):
  Config (templates = templates)
  Config.set ("xxpaper/version", __version__)
