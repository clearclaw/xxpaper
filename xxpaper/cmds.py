#! /usr/bin/env python

import clip, logging, logtool
from .main import app_main

LOG = logging.getLogger (__name__)
OPTIONS = ["help", "debug", "nosentry", "verbose", "version"]

# pylint: disable=import-outside-toplevel
@app_main.subcommand (
  name = "check",
  description = "Check formatting of game file",
  inherits = OPTIONS)
@clip.arg (name = "template", default = None,
           help = "XXPaper game file", required = True)
@logtool.log_call
def check (**kwargs):
  from .cmd_check import do
  do (**kwargs)

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
  from .cmd_dump import do
  do (**kwargs)

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
  from .cmd_lookup import do
  do (**kwargs)

@app_main.subcommand (
  name = "make",
  description = "Make game files",
  inherits = OPTIONS)
@logtool.log_call
def make (**kwargs): # pylint: disable=unused-argument
  pass

@make.subcommand (
  name = "assets",
  description = "Make assets artfile for a game",
  inherits = OPTIONS)
@clip.flag ("-c", "--cutline", name = "cutline",
            default = False, help = "Draw cutlines")
@clip.opt ("-f", "--filter", name = "filter",
           help = "Only these asset-types")
@clip.opt ("-p", "--paper", name = "paper",
           default = "A4", help = "Paper size (A4, letter)")
@clip.opt ("-r", "--repeat", name = "repeat",
           default = "", help = "Make repeats of these (comma separated)")
@clip.arg (name = "templates",
           help = "XXPaper game files (comma separated)", required = True)
@clip.arg (name = "outfile",
           help = "File to produce (default: first template .pdf)",
           required = False)
@logtool.log_call
def assets (**kwargs):
  from .cmd_assets import do
  do (**kwargs)

@make.subcommand (
  name = "cards",
  description = "Make card artfiles for a game",
  inherits = OPTIONS)
@clip.flag ("-c", "--cutline", name = "cutline",
            default = False, help = "Draw cutlines")
@clip.opt ("-f", "--filter", name = "filter",
           help = "Only these asset-types")
@clip.arg (name = "templates",
           help = "XXPaper game files (comma separated)", required = True)
@clip.arg (name = "outfile",
           help = "File prefix(es) to produce (default: first template .pdf)",
           required = False)
@logtool.log_call
def cards (**kwargs):
  from .cmd_cards import do
  do (**kwargs)
