#! /usr/bin/env python

from __future__ import absolute_import
import clip, logging, logtool, raven, sys
from path import Path
from .config import Config
from . import __version__

logging.basicConfig (level = logging.WARN)
LOG = logging.getLogger (__name__)
APP = clip.App (name = "xxpaper")
Config.set ("xxpaper", {})

@logtool.log_call
def option_logging (flag): # pylint: disable=unused-argument
  logging.root.setLevel (logging.DEBUG)

@logtool.log_call
def option_nosentry (value):
  Config._nosentry = value # pylint: disable=protected-access

@logtool.log_call
def option_verbose (value):
  Config._verbose = value # pylint: disable=protected-access

@logtool.log_call
def option_version (opt): # pylint: disable=unused-argument
  clip.echo ("Version: %s" %  __version__)
  sys.exit (0)

@APP.main (name = Path (sys.argv[0]).basename (),
           description = "18xx rapid prototyping tool",
           tree_view = "-H")
@clip.flag ("-H", "--HELP",  help = "Help for all sub-commands")
@clip.flag ("-D", "--debug", name = "debug", help = "Enable debug logging",
            callback = option_logging)
@clip.flag ("-N", "--nosentry", name = "nosentry",
            help = "Do not send exception reports to the developers",
            callback = option_logging)
@clip.flag ("-v", "--verbose", help = "Show keys as they are resolved",
            callback = option_verbose)
@clip.flag ("-V", "--version", help = "Report installed version",
            callback = option_version)
@logtool.log_call
def app_main (*args, **kwargs): # pylint: disable=unused-argument
  if kwargs["debug"]:
    logging.basicConfig (level = logging.DEBUG)

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
    print >> sys.stderr, ("Something broke!")
    if not (getattr (Config, "_nosentry", False)
            or Config.get ("user/nosentry", params = {"default": True})):
      client = raven.Client (
        "https://250e838eaff24eee9461682bc7160904"
        ":b455442d9dcb4773a82786844f430386@sentry.io/127918")
      h = client.captureException ()
      print >> sys.stderr, "\t Sentry filed: %s" % h
    sys.exit (1)

if __name__ == "__main__":
  main ()
