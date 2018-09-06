#! /usr/bin/env python

from __future__ import absolute_import
import contextlib, logging, logtool, math
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
    l = key.split ("/")
    if not l[0].endswith ("_clone"):
      return Config.get (key, params = params)
    # Special case hack to make clone objects key transparent
    flag = float ("nan") # Something that should be never used
    d = params.get ("default", flag)
    params["default"] = flag
    rc = Config.get (key, params = params)
    if not isinstance (rc, float) or not math.isnan (rc):
      return rc
    of = Config.get (l[0] + "/of", params = params)
    params["default"] = d
    rc = Config.get (of + "/" + l[1], params = params)
    return rc

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
    dash = self.value (key + "/dash", default = None)
    dash_phase = self.value (key + "/dash_phase", default = 0)
    if dash is not None :
      self.canvas.setDash (dash, phase = dash_phase)
    line_cap = self.value (key + "/line_cap", default = None)
    if line_cap is not None:
      self.canvas.setLineCap (line_cap)
    line_join = self.value (key + "/line_join", default = None)
    if line_join is not None:
      self.canvas.setLineNJoin (line_join)
    fill = self.value (key + "/fill", default = None)
    if fill is not None:
      self.canvas.setFillColorRGB (*fill)
    stroke = self.value (key + "/stroke", default = None)
    if stroke is not None:
      self.canvas.setStrokeColorRGB (*stroke)
    width = self.value (key + "/width", default = None)
    if width is not None:
      self.canvas.setLineWidth (width)

  @logtool.log_call
  def draw_box (self, key):
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
    path = self.canvas.beginPath ()
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
  def draw_circle (self, key):
    x = self.value (key + "/x", default = 0)
    y = self.value (key + "/y", default = 0)
    radius = self.value (key + "/radius")
    fill = self.value (key + "/fill", default = None)
    stroke = self.value (key + "/stroke", default = None)
    self.canvas.circle (x, y, radius,
                        fill = 1 if fill else 0,
                        stroke = 1 if stroke else 0)

  @logtool.log_call
  def path_circle (self, key):
    path = self.canvas.beginPath ()
    x = self.value (key + "/x", default = 0)
    y = self.value (key + "/y", default = 0)
    radius = self.value (key + "/radius")
    path.circle (x, y, radius)
    return path

  @logtool.log_call
  def draw_shape (self, key):
    path = self.path_shape (key)
    fill = self.value (key + "/fill", default = 0)
    fill_mode = self.value (key + "/fill_mode", default = None)
    stroke = self.value (key + "/stroke", default = 0)
    self.canvas.drawPath (path,
                          fill = 1 if fill else 0,
                          fillMode = 1 if fill_mode else 0,
                          stroke = 1 if stroke else 0)

  @logtool.log_call
  def path_shape (self, key):
    path = self.path_line (key)
    path.close ()
    return path

  @logtool.log_call
  def draw_line (self, key):
    path = self.path_line (key)
    stroke = self.value (key + "/stroke", default = 0)
    self.canvas.drawPath (path, stroke = 1 if stroke else 0)

  @logtool.log_call
  def path_line (self, key):
    path = self.canvas.beginPath ()
    x = self.value (key + "/x", default = 0)
    y = self.value (key + "/y", default = 0)
    path.moveTo (x, y)
    for point in self.value (key + "/points", default = []):
      fn = path.lineTo if len (point) == 2 else path.curveTo
      p = point if len (point) == 2 else [b for a in point for b in a]
      fn (*p)
    return path

  @logtool.log_call
  def draw_clone (self, key):
    of = self.value (key + "/of")
    with self._with_context ():
      self._inset (key)
      self._set_properties (key)
      suffix = of.split ("_")[-1]
      fn = getattr (self, "draw_" + suffix)
      fn (key)

  @logtool.log_call
  def path_clone (self, key):
    of = self.value (key + "/of")
    od = self.value (key + "/.")
    cd = dict (self.value (of + "/."))
    for k, v in cd.items ():
      if k not in od:
        od[k] = v # Nested clones will not merge the full stack
    # No ROTATE
    suffix = of.split ("_")[-1]
    fn = getattr (self, "path_" + suffix)
    return fn (key)

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
    with self._with_context ():
      self.canvas.clipPath (cut, fill = 0, stroke = 0)
      self._render_elements (self.value (typ + "/EMBED_ELEMENTS"))

  @logtool.log_call
  def draw_embed (self, key):
    typ = self.value (key + "/typ")
    name = self.value (key + "/name", default = self.name)
    n = self.value (key + "/n", default = self.n)
    tile = Tile (typ, self.canvas, name, n)
    tile._draw_embed (typ) # pylint: disable=protected-access

  @logtool.log_call
  def _render_elements (self, elements):
    for key in elements:
      if self.value (key + "/suppress", default = False):
        continue
      if key == "rotate":
        x = self.value (self.tile_type + "/x")
        margin = self.value (self.tile_type + "/margin")
        self.canvas.translate (x - (2 * margin), 0)
        self.canvas.rotate (90)
        continue
      with self._with_context ():
        self._inset (key)
        self._set_properties (key)
        suffix = key.split ("_")[-1]
        fn = getattr (self, "draw_" + suffix)
        fn (key)

  @logtool.log_call
  def render (self):
    self._render_elements (self.value (self.typ + "/ELEMENTS"))

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
