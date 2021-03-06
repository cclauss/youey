#coding: utf-8
from youey.util.prop import *
from youey.constants import *
from youey.transform import *

def _get(obj, name):
  prop = _prop(obj, name)
  return prop.fget(obj)
  
def _set(obj, name, value):
  prop = _prop(obj, name)
  prop.fset(obj, value)
  
def _prop(obj, name):
  props = {
    LEFT: type(obj).left,
    X: type(obj).x,
    RIGHT: type(obj).right,
    WIDTH: type(obj).width,
    MAX_WIDTH: type(obj).max_width,
    MIN_WIDTH: type(obj).min_width,
    INNER_WIDTH: type(obj).inner_width,
    CENTER: type(obj).center,
    TOP: type(obj).top,
    Y: type(obj).y,
    BOTTOM: type(obj).bottom,
    HEIGHT: type(obj).height,
    MAX_HEIGHT: type(obj).max_height,
    MIN_HEIGHT: type(obj).min_height,
    INNER_HEIGHT: type(obj).inner_height,
    MIDDLE: type(obj).middle,
    GRID_SIZE: type(obj).grid_size,
    SIZE: type(obj).size
  }
  return props[name]

class PublicLayoutProperties():
  
  @property
  def left(self):
    return self._getr(LEFT)
    
  @left.setter
  def left(self, value):
    self._setr(LEFT, value)
    
  x = left
    
  @property
  def top(self):
    return self._getr(TOP)
    
  @top.setter
  def top(self, value):
    self._setr(TOP, value)
    
  y = top
    
  @property
  def width(self):
    return self._getr(WIDTH)
    
  @width.setter
  def width(self, value):
    self._setr(WIDTH, value)
    
  @prop
  def max_width(self, *args, base_prop):
    if args:
      self._setr(MAX_WIDTH, args[0])
    else:
      return self._getr(MAX_WIDTH)
      
  @prop
  def min_width(self, *args, base_prop):
    if args:
      self._setr(MIN_WIDTH, args[0])
    else:
      return self._getr(MIN_WIDTH)
    
  @property
  def inner_width(self):
    return self._getr(WIDTH) #, inner=True)
    
  @property
  def height(self):
    return self._getr(HEIGHT)
    
  @height.setter
  def height(self, value):
    self._setr(HEIGHT, value)
    
  @prop
  def max_height(self, *args, base_prop):
    if args:
      self._setr(MAX_HEIGHT, args[0])
    else:
      return self._getr(MAX_HEIGHT)
      
  @prop
  def min_height(self, *args, base_prop):
    if args:
      self._setr(MIN_HEIGHT, args[0])
    else:
      return self._getr(MIN_HEIGHT)
    
  @property
  def inner_height(self):
    return self._getr(HEIGHT) #, inner=True)
    
  @property
  def right(self):
    return self._getr(RIGHT)
    
  @right.setter
  def right(self, value):
    self._setr(RIGHT, value, reverse_prop=WIDTH)
    
  @property
  def bottom(self):
    return self._getr(BOTTOM)
    
  @bottom.setter
  def bottom(self, value):
    self._setr(BOTTOM, value, reverse_prop=HEIGHT)
    
  @property
  def center(self):
    return self._getr(LEFT, WIDTH)
    
  @center.setter
  def center(self, value):
    value = self._set_anchor(CENTER, value)
    if value is None:
      value = 'auto'
    else:
      value = value - self.width/2
    self._js.set_style('left', value)
    
  @property
  def middle(self):
    return self._getr(TOP, HEIGHT)

  @middle.setter
  def middle(self, value):
    value = self._set_anchor(MIDDLE, value)
    if value is None:
      value = 'auto'
    else:
      value = value - self.height/2
    self._js.set_style('top', value)
    
  @prop
  def frame(self, *args, base_prop):
    if args:
      self.left, self.top, self.width, self.height = args[0]
    else:
      return (self.left, self.top, self.width, self.height)
    
  @prop
  def size(self, *args, base_prop):
    if args:
      value = args[0]
      value = self._set_anchor(SIZE, value)
      self.width, self.height = value
    else:
      return self._getr(SIZE)
    
  @prop
  def transform(self, *args, base_prop):
    if args:
      t = args[0]
      setattr(self, base_prop, t)
      self._js.set_style('transform', t.to_css())
    else:
      return getattr(self, base_prop, Transform())
      
  def rotate_by(self, angle_deg):
    t = self.transform
    t.rotate_by(angle_deg)
    self.transform = t
    
  def scale_by(self, scale_delta):
    t = self.transform
    t.scale_by(scale_delta)
    self.transform = t
    
  @prop
  def rotation(self, *args, base_prop):
    if args:
      angle_deg = args[0]
      t = self.transform
      t.unmatrix()
      current_deg = t.rotation
      t.rotate_by(-current_deg)
      t.rotate_by(angle_deg)
      self.transform = t
    else:
      t = self.transform
      t.unmatrix()
      return t.rotation
      
  @prop
  def scale(self, *args, base_prop):
    if args:
      scale_abs = args[0]
      t = self.transform
      t.unmatrix()
      current_scale = t.scale
      t.scale_by(-current_scale)
      t.scale_by(scale_abs)
      self.transform = t
    else:
      t = self.transform
      t.unmatrix()
      return t.scale
    
  @property
  def grid_size(self):
    raise RuntimeError('This property should only be accessed in ContainerView')
    
    
  '''
  @prop
  def margin_left(self, *args, base_prop):
    if args:
      self._inner.set_style('left', args[0])
    else:
      return self._inner.abs_style('left')
      
  @prop
  def margin_top(self, *args, base_prop):
    if args:
      self._inner.set_style('top', args[0])
    else:
      return self._inner.abs_style('top')
      
  @prop
  def margin_right(self, *args, base_prop):
    if args:
      self._inner.set_style('right', args[0])
    else:
      return self._inner.abs_style('right')
      
  @prop
  def margin_bottom(self, *args, base_prop):
    if args:
      self._inner.set_style('bottom', args[0])
    else:
      return self._inner.abs_style('bottom')
  '''

  @prop
  def margin(self, *args, base_prop):
    if args:  
      self.margin_top, self.margin_right, self.margin_bottom, self.margin_left = self._parse_multiple_edges(args[0])
      js = f'{self.margin_top}px {self.margin_right}px {self.margin_bottom}px {self.margin_left}px'
      self._js.set_style('margin', js)
    else:
      return (self.margin_top, self.margin_right, self.margin_bottom, self.margin_left)

  @property
  def padding(self):
    return (self.padding_top, self.padding_right, self.padding_bottom, self.padding_left)
    
  @padding.setter
  def padding(self, value):
    self.padding_top, self.padding_right, self.padding_bottom, self.padding_left = self._parse_multiple_edges(value)
    js = f'{self.padding_top}px {self.padding_right}px {self.padding_bottom}px {self.padding_left}px'
    self._js.set_style('padding', js)

  def _parse_multiple_edges(self, value):
    if type(value) in [int, float]:
      values = (value,)*4
    elif type(value) in [list, tuple]:
      if len(value) == 1:
        values = (value[0],)*4
      elif len(value) == 2:
        values = (value[0], value[1])*2
      elif len(value) == 3:
        values = (value[0], value[1], value[2], value[1])
      elif len(value) == 4:
        values = value
    return values
    
  @prop
  def scrollable(self, *args, base_prop):
    if args:
      value = args[0]
      if value:
        self._js.set_style('pointerEvents', 'auto')
        self._js.set_style('-webkit-overflow-scrolling', 'touch')
      if not value:
        self._js.set_style('overflow', 'hidden')
      elif value == HORIZONTAL:
        self._js.set_style('overflowY', 'hidden')
        self._js.set_style('overflowX', 'auto')
      elif value == VERTICAL:
        self._js.set_style('overflowX', 'hidden')
        self._js.set_style('overflowY', 'auto')
      elif value == True:
        self._js.set_style('overflow', 'auto')
      else:
        raise ValueError('Unknown value for scrollable: ' + str(value))
      setattr(self, base_prop, value)
    else:
      return getattr(self, base_prop, None)

class Refresh():
  "When used to set a property value, instead refreshes from the anchor value."
  
class LayoutMacros():
  
  def dock_all(self, offset=0):
    self.left = self.top = self.right = self.bottom = offset
    return self
  
  def dock_left(self, offset=0):
    self.left = self.top = self.bottom = offset
    return self
  
  def dock_top(self, offset=0):
    self.left = self.top = self.right = offset
    return self
    
  def dock_right(self, offset=0):
    self.top = self.right = self.bottom = offset
    return self
    
  def dock_bottom(self, offset=0):
    self.left = self.bottom = self.right = offset
    return self
    
  def dock_sides(self, offset=0):
    self.left = self.right = offset
    return self
    
  def dock_top_and_bottom(self, offset=0):
    self.top = self.bottom = offset
    return self
    
  def dock_center(self):
    self.center = Center(self.parent)
    self.middle = Middle(self.parent)
    return self

  # Layout helpers
  @property
  def orientation(self):
    if self.width > self.height:
      return LANDSCAPE
    elif self.width < self.height:
      return PORTRAIT
    else:
      return SQUARE
      
  @property
  def is_landscape(self):
    return self.orientation == LANDSCAPE
    
  @property
  def is_portrait(self):
    return self.orientation == PORTRAIT

  
class LayoutHelpers():
  
  def _getr(self, prop, prop2=None, inner=False):
    #elem = self._inner if inner else self._js
    prop = to_camel_case(prop)
    value = self._js.abs_style(prop)
    if prop2:
      prop2 = to_camel_case(prop2)
      value2 = self._js.abs_style(prop2)
      value = value + value2/2
    return value
    
  def _setr(self, prop, value, reverse_prop=None, inner=False):
    original_intent = value
    if reverse_prop and isinstance(value, At):
      value.receiver = (self, reverse_prop)
    value = self._set_anchor(prop, value)
    if value is None:
      value = 'auto'
    if type(value) is not tuple:
      prop = to_camel_case(prop)
      self._js.set_style(prop, value)
    if original_intent is not Refresh:
      self.root._update_all_dependencies(self)
  
  def _set_anchor(self, prop, value):
    if value == Refresh:
      return self._resolve_anchor(prop)
    self._anchors[prop] = value
    if isinstance(value, At):
      value.ref._dependents.add((self, prop))
    actual_value = self._resolve_anchor(prop)
    return actual_value
    
  def _resolve_anchor(self, prop):
    anchor = self._anchors.get(prop, None)
    if anchor is None: return None
    if type(anchor) in [int, float, tuple]:
      return anchor
    else:
      return anchor.resolve()
    
  def _refresh(self, prop):
    _set(self, prop, Refresh)
    
    
class LayoutProperties(PublicLayoutProperties, LayoutMacros, LayoutHelpers):
  pass
    
class At():
  
  from_origin = True
  
  def __init__(self, ref, prop, multiplier=None, offset=0):
    self.ref = ref
    self.prop = prop
    self.offset = offset
    self.multiplier = multiplier
    self.edge_prop = None
    self.receiver = None

  def resolve(self):
    result = _get(self.ref, self.prop)
    if type(result) is tuple:
      return result
    if isinstance(self, FromEdge):
      result = _get(self.ref.parent, self.invert_prop) - result
    if self.receiver and not isinstance(self, NotCoordinateValue): # is inverted
      result = _get(self.receiver[0].parent, self.receiver[1]) - result
    if type(self.multiplier) is str:
      self.multiplier = float(self.multiplier.strip('%'))/100
    '''
    if type(result) is tuple:
      result = tuple((elem * self.multiplier or 1 for elem in result))
      result = tuple((elem + self.offset for elem in result))
    else:
    '''
    multiplier = self.multiplier if not callable(self.multiplier) else self.multiplier()
    result *= multiplier or 1
    result += self.offset
    return result
    
  def from_edge(self, result):
    return _get(self.ref, self.edge_prop) - result

  
'''
class Value(At):
  def __init__(self, ref, value):
    self.ref = ref
    self.value = value
    self.offset = 0
    self.multiplier = 1
    self.edge_prop = None
    self.receiver = None
    
  def resolve(self):
    return self.value
'''

class Top(At):
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, TOP, multiplier, offset)
class Left(At):
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, LEFT, multiplier, offset)
    
class NotCoordinateValue(At): pass
  
class Width(NotCoordinateValue):
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, WIDTH, multiplier, offset)
class Height(NotCoordinateValue):
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, HEIGHT, multiplier, offset)
    
class Center(Width):
  def __init__(self, ref, offset=0):
    super().__init__(ref, multiplier=0.5, offset=offset)
class Middle(Height):
  def __init__(self, ref, offset=0):
    super().__init__(ref, multiplier=0.5, offset=offset)

class InnerWidth(NotCoordinateValue):
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, INNER_WIDTH, multiplier, offset)
class InnerHeight(NotCoordinateValue):
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, INNER_HEIGHT, multiplier, offset)

class FromEdge(At): pass

class Right(FromEdge):
  invert_prop = WIDTH
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, RIGHT, multiplier, offset)
class Bottom(FromEdge):
  invert_prop = HEIGHT
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, BOTTOM, multiplier, offset)

class GridSize(At):
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, GRID_SIZE, multiplier, offset)

def _to_edge(view, prop, value):
  return _get(view, prop) - value
  
class AddOn(At):
  
  def __init__(self, *anchors):
    self._anchors = anchors
    
class Min(AddOn):
  
  def resolve(self):
    return min([anchor.resolve() for anchor in self._anchors])
    
class Max(AddOn):
  
  def resolve(self):
    return max([anchor.resolve() for anchor in self._anchors])
  
class Size(At):
  def __init__(self, ref, multiplier=None, offset=0):
    super().__init__(ref, SIZE, multiplier, offset)
  

if __name__ == '__main__':
  pass
