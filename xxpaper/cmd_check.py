#! /usr/bin/env python

from __future__ import absolute_import
import codecs, logging, logtool, json, toml, yaml
from path import Path
from .config import Config

LOG = logging.getLogger (__name__)

@logtool.log_call
def do (**kwargs):
  exts = ("", ".xxp", ".json", ".yaml", ".yml", ".toml")
  fname = kwargs["template"]
  d = None
  for ext in exts:
    f = Path ("%s%s" % (fname, ext))
    if f.isfile ():
      try:
        print "Trying to load %s as JSON." % f
        d = json.loads (codecs.open (f, encoding='utf-8').read ())
        print "\tSuccessfully loaded as JSON."
        if Config._verbose: # pylint: disable=protected-access
          print "\nResult:\n========\n\n%s" % json.dumps (d, indent = 2)
      except Exception as e:
        print "\tFailed: %s" % e
        try:
          print "Trying to load %s as YAML." % f
          d = yaml.safe_load (codecs.open (f, encoding='utf-8'))
          print "\tSuccessfully loaded as YAML."
          if Config._verbose: # pylint: disable=protected-access
            print "\nResult:\n========\n\n%s" % yaml.dump (
              d, width = 70, indent = 2, default_flow_style = False)
        except Exception as e:
          print "\tFailed: %s" % e
          try:
            print "Trying to load %s as TOML." % f
            d = toml.loads (codecs.open (f, encoding='utf-8').read ())
            print "\tSuccessfully loaded as TOML."
            if Config._verbose: # pylint: disable=protected-access
              print "\nResult:\n========\n\n%s" % toml.dumps (d)
          except Exception as e:
            print "\tFailed: %s" % e
