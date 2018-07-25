#! /usr/bin/env python

from __future__ import absolute_import
import contextlib, logging, logtool
from .config import Config

LOG = logging.getLogger (__name__)

class Tile (object):

  @logtool.log_call
  def __init__ (self, asset, canvas, name, n):
    if asset:
      catalogue = Config.get ("CATALOGUE/" + asset)
    self.asset = asset
    self.tile_type = catalogue["tile_type"] if asset else "-missing-"
    self.klass = catalogue["klass"] if asset else "-missing-"
    self.typ = catalogue["typ"] if asset else "-missing-"
    self.canvas = canvas
    self.name = name
    self.n = n

  #@logtool.log_call
  def value (self, key, **kwargs):
    params = {
      "klass": self.klass,
      "typ": self.typ,
      "name": self.name,
      "n": self.n,
    }
    params.update (kwargs)
    return Config.get (key, params = params)

  @contextlib.contextmanager
  @logtool.log_call
  def _with_context (self):
    self.canvas.saveState ()
    yield
    self.canvas.restoreState ()

  @logtool.log_call
  def _inset (self, key, suffix = "_inset"):
    x = self.value (key + "/x" + suffix, default = None)
    y = self.value (key + "/y" + suffix, default = None)
    if x is not None and y is not None:
      self.canvas.translate (x, y)

  @logtool.log_call
  def _set_properties (self, key):
    fill = self.value (key + "/fill", default = None)
    stroke = self.value (key + "/stroke", default = None)
    width = self.value (key + "/width", default = None)
    if stroke is not None:
      self.canvas.setStrokeColorRGB (*stroke)
    if width is not None:
      self.canvas.setLineWidth (width)
    if fill is not None:
      self.canvas.setFillColorRGB (*fill)

  @logtool.log_call
  def draw_box (self, key):
    if self.value (key + "/suppress", default = False):
      return
    with self._with_context ():
      self._inset (key)
      self._set_properties (key)
      x = self.value (key + "/x")
      y = self.value (key + "/y")
      fill = self.value (key + "/fill", default = None)
      stroke = self.value (key + "/stroke", default = None)
      radius = self.value (key + "/radius", default = None)
      if radius is None:
        self.canvas.rect (0, 0, x, y,
                          fill = 0 if fill is None else 1,
                          stroke = 0 if stroke is None else 1)
      else:
        self.canvas.roundRect (0, 0, x, y,
                               radius,
                               fill = 0 if fill is None else 1,
                               stroke = 0 if stroke is None else 1)

  @logtool.log_call
  def path_box (self, key):
    if self.value (key + "/suppress", default = False):
      return self.canvas.beginPath  ()
    path = self.canvas.beginPath  ()
    x = self.value (key + "/x")
    y = self.value (key + "/y")
    radius = self.value (key + "/radius", default = None)
    if radius is None:
      path.rect (0, 0, x, y)
    else:
      path.roundRect (0, 0, x, y, radius)
    return path

  @logtool.log_call
  def draw_text (self, key):
    if self.value (key + "/suppress", default = False):
      return
    with self._with_context ():
      self._inset (key)
      x = self.value (key + "/x", default = 0)
      y = self.value (key + "/y", default = 0)
      txt = self.value (key + "/text")
      h_center = self.value (key + "/h_center", default = 1)
      v_center = self.value (key + "/v_center", default = 1)
      typeface = self.value (key + "/typeface")
      size = self.value (key + "/size")
      line_height = self.value (key + "/line_height", default = size)
      if txt in ("", None):
        return
      lines = txt.split ("\n")
      while lines[-1].strip () == "":
        lines.pop ()
      while lines[0].strip () == "":
        lines = lines[1:]
      if v_center == -1:
        y += line_height * (len (lines) - 1)
      elif v_center == 0:
        y += line_height * (float (len (lines) - 1) / 2.0)
      elif v_center == 1:
        pass
      # self.canvas.translate (x, y)
      self.canvas.setFont (typeface, size)
      self._set_properties (key)
      for t in lines:
        if h_center == -1:
          self.canvas.drawRightString (x, y, t)
        elif h_center == 0:
          self.canvas.drawCentredString (x, y, t)
        elif h_center == 1:
          self.canvas.drawString (x, y, t)
        else:
          raise ValueError
        y -= line_height

  @logtool.log_call
  def path_text (self, key):
    self.draw_text (key)

  @logtool.log_call
  def draw_circle (self, key, x = None, y = None):
    if self.value (key + "/suppress", default = False):
      return
    with self._with_context ():
      self._inset (key)
      x = x if x is not None else self.value (key + "/x")
      y = y if y is not None else self.value (key + "/y")
      radius = self.value (key + "/radius")
      self._set_properties (key)
      fill = self.value (key + "/fill", default = None)
      stroke = self.value (key + "/stroke", default = None)
      self.canvas.circle (x, y, radius,
                          fill = 1 if fill else 0,
                          stroke = 1 if stroke else 0)

  @logtool.log_call
  def path_circle (self, key, x = None, y = None):
    if self.value (key + "/suppress", default = False):
      return self.canvas.beginPath  ()
    path = self.canvas.beginPath  ()
    x = x if x is not None else self.value (key + "/x")
    y = y if y is not None else self.value (key + "/y")
    radius = self.value (key + "/radius")
    path.circle (x, y, radius)
    return path

  @logtool.log_call
  def draw_rotate (self, key): # pylint: disable=unused-argument
    x = self.value (self.tile_type + "/x")
    margin = self.value (self.tile_type + "/margin")
    self.canvas.translate (x - (2 * margin), 0)
    self.canvas.rotate (90)

  @logtool.log_call
  def path_rotate (self, key):
    pass

  @logtool.log_call
  def _get_cutpath (self, typ):
    cutkey = self.value (typ + "/EMBED_CUT_ELEMENT")
    s = cutkey.split ("_")[-1]
    if s == "text": # Paths don't support text
      raise ValueError ("EMBED_CUT_ELEMENT cannot be text: " + s)
    f = getattr (self, "path_" + s)
    cutpath = f (cutkey)
    cutpath.isClipPath = True
    return cutpath

  @logtool.log_call
  def _draw_embed (self, typ):
    cut = self._get_cutpath (typ)
    for key in self.value (typ + "/EMBED_ELEMENTS"):
      with self._with_context ():
        s = key.split ("_")[-1]
        if s in ("pop", "push", "rotate", "scale", "text", "xlate"):
          # Because they're not supported by paths
          fn = getattr (self, "draw_" + s)
          fn (key)
          continue
        fn = getattr (self, "path_" + s)
        path = fn (key)
        self.canvas.clipPath (cut, fill = 0, stroke = 0)
        self._inset (key)
        self._set_properties (key)
        fill = (self.value (key + "/fill", default = None) is not None)
        stroke = (self.value (key + "/stroke", default = None) is not None)
        self.canvas.drawPath (path, fill = fill, stroke = stroke)

  @logtool.log_call
  def draw_embed (self, key):
    if self.value (key + "/suppress", default = False):
      return
    typ = self.value (key + "/embed")
    name = self.value (key + "/name", default = self.name)
    n = self.value (key + "/n", default = self.n)
    with self._with_context ():
      self._inset (key)
      tile = Tile (typ, self.canvas, name, n)
      tile._draw_embed (typ) # pylint: disable=protected-access

  @logtool.log_call
  def render (self):
    for e in self.value (self.typ + "/ELEMENTS"):
      suffix = e.split ("_")[-1]
      fn = getattr (self, "draw_" + suffix)
      fn (e)

  @logtool.log_call
  def cutline (self):
    e = self.value (self.typ + "/CUT_ELEMENT")
    suffix = e.split ("_")[-1]
    fn = getattr (self, "draw_" + suffix)
    fn (e)

@logtool.log_call
def items (canvas, asset):
  catalogue = Config.get ("CATALOGUE/" + asset)
  if (catalogue is None
      or catalogue.get ("name_index") is None
      or Config.get (catalogue["name_index"]) is None):
    return []
  rc = []
  for name in sorted (Config.get (catalogue["name_index"]).keys ()):
    if catalogue["instance_index"] is not None:
      ndx = Tile (asset, canvas, name, 0).value (
          catalogue["instance_index"])
      if ndx is not None:
        for n in sorted (ndx.keys ()):
          rc.append (Tile (asset, canvas, name, n))
    else:
      rc.append (Tile (asset, canvas, name, 0))
  return rc
