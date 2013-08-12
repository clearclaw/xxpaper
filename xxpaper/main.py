#! /usr/bin/env python

import os, sys
from configobj import ConfigObj
import xxpaper

def make (conf, xtype, page, fname):
  with getattr (xxpaper, xtype.capitalize ()) (conf, xtype, page, fname) as t:
    t.make ()
  print fname

def error ():
  print >> sys.stderr, ("Syntax: %s <cfg_file> [[[type] page] output_file]"
                        % sys.argv[0])
  sys.exit (0)

def main ():
  if len (sys.argv) == 1:
    error ()
  if len (sys.argv) >= 2:
    cfg_name = sys.argv[1]
    conf = ConfigObj (cfg_name)
    if not os.path.isfile (cfg_name):
      print >> sys.stderr, ("Error: Cannot access configuration file: %s"
                            % cfg_name)
      sys.exit (2)
  if len (sys.argv) >= 3:
    xtype = sys.argv[2]
    if not xtype in conf.sections:
      print >> sys.stderr, ("Error: Cannot find section %s in file: %s"
                            % (xtype, cfg_name))
      sys.exit (1)
  if len (sys.argv) >= 4:
    page = sys.argv[3]
    if not page in conf[xtype].sections:
      print >> sys.stderr, ("Error: Cannot find section %s.%s in file: %s"
                            % (xtype, page, cfg_name))
      sys.exit (1)
  if len (sys.argv) >= 5:
    error ()
  paper = conf["DEFAULT"]["paper"]
  if len (sys.argv) == 2:
    for t in conf.sections:
      if t == "DEFAULT":
        continue
      for p in conf[t].sections:
        make (conf, t, p, os.path.join ("./", "%s_%s-%s.ps" % (t, p, paper)))
  elif len (sys.argv) == 3:
    for p in conf[xtype].sections:
      make (conf, xtype, p, os.path.join ("./", "%s_%s-%s.ps" % (xtype, p, paper)))
  else:
    make (conf, xtype, page, os.path.join ("./", "%s_%s-%s.ps"
                                           % (xtype, page, paper)))
  sys.exit (0)

if __name__ == '__main__':
  main ()
