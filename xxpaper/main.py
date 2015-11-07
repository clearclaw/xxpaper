#! /usr/bin/env python

import argparse, itertools, jinja2, os, pkg_resources, StringIO, sys
from configobj import ConfigObj
import xxpaper

def make (cfgs, sheet, page, fname):
  with getattr (xxpaper, sheet.capitalize ()) (cfgs, sheet, page, fname) as t:
    t.make ()
  print fname

def get_cfgval (cfgs, sheet, name):
  for cfg in itertools.chain (cfgs):
    try:
      return cfg[sheet][name]
    except: # pylint: disable=bare-except
      pass
    try:
      return cfg["DEFAULT"][name]
    except: # pylint: disable=bare-except
      pass
  print >> sys.stderr, ("Error: Cannot find the value of: %s"
                        % name)
  sys.exit (1)

def read_overrides (values):
  return ConfigObj (itertools.chain (["[DEFAULT]",], values.split (",")))

def read_config (fname):
  cfg = file (fname).read ()
  template = jinja2.Template (cfg)
  xxp = StringIO.StringIO (template.render ())
  # with open (fname + "-cfg", "w") as f:
  #  f.write (xxp.getvalue ())
  conf = ConfigObj (xxp.readlines ())
  # conf = ConfigObj (file (fname).readlines ())
  if "DEFAULT" not in conf.sections:
    conf["DEFAULT"] = {}
  conf["DEFAULT"]["source_filename"] = "File: %s" % fname
  return conf

def process_args ():
  parser = argparse.ArgumentParser (
    description = "18xx rapid prototyping tool.")
  parser.add_argument (
    "-o", "--override", metavar = "ASSIGNMENTS", dest = "override",
    type = read_overrides, required = False,
    help = "Individual settings to override all others")
  parser.add_argument (
    "-l", "--local", metavar = "FILE", dest = "local",
    type = read_config, required = False,
    help = "Option file to override game configuration and DEFAULTs")
  parser.add_argument (nargs = 1, metavar = "FILE", dest = "conf",
                       type = read_config, help = "Game configuration file")
  parser.add_argument (nargs = '?', metavar = "SECTION", dest = "sheet",
                       default = None, help = "Section to render")
  parser.add_argument (nargs = '?', metavar = "PAGE", dest = "page",
                       default = None, help = "Page in section to render")
  args = parser.parse_args ()
  args.conf = args.conf[0] # nargs=1 makes it a silly list
  #  args.conf.my_name = "user_conf"
  s = pkg_resources.resource_string ("xxpaper", "DEFAULT.conf")
  args.default = ConfigObj (s.split ("\n"))
  # args.default.my_name = "default_conf"
  # args.override.my_name = "cli_conf"
  args.runtime = ConfigObj (["[DEFAULT]",])
  if args.sheet and args.sheet not in args.conf.sections:
    print >> sys.stderr, ("Error: Cannot find section %s in game file."
                          % args.sheet)
    sys.exit (1)
  if (args.sheet and args.page
      and args.page not in args.conf[args.sheet].sections):
    print >> sys.stderr, ("Error: Cannot find section %s.%s in game file."
                          % (args.sheet, args.page))
    sys.exit (2)
  return args

def main ():
  args = process_args ()
  cfgs = [x for x in [args.runtime, args.override, args.local,
                      args.conf, args.default] if not None]
  papers = get_cfgval (cfgs, "DEFAULT", "papers")
  outlines = get_cfgval (cfgs, "DEFAULT", "outlines")
  for paper in papers:
    args.runtime["DEFAULT"]["paper"] = paper
    for outline in outlines:
      args.runtime["DEFAULT"]["outline"] = outline
      o = "outline" if outline == "1" else "nooutline"
      for sheet in args.conf.sections:
        if sheet == "DEFAULT" or (args.sheet and sheet != args.sheet):
          continue
        for page in args.conf[sheet].sections:
          if args.page and page != args.page:
            continue
          make (cfgs, sheet, page,
                os.path.join ("./", "%s_%s-%s-%s.ps"
                              % (sheet, page, o, paper)))
  sys.exit (0)

if __name__ == '__main__':
  main ()
