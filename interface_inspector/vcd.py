from enum import Enum
from bisect import bisect_right
from pyDigitalWaveTools.vcd.parser import VcdParser, VcdVarScope

class ValueFormat(Enum):
  BINARY      = 0
  OCTAL       = 1
  DECIMAL     = 2
  HEXADECIMAL = 3

class VCDValue:
  def __init__(self, value, format:ValueFormat):
    if isinstance(value,int):
      self.value = value
    elif isinstance(value,str):
      match format:
        case ValueFormat.BINARY:
          self.value = int(value,2)
        case ValueFormat.OCTAL:
          self.value = int(value,8)
        case ValueFormat.DECIMAL:
          self.value = int(value,10)
        case ValueFormat.HEXADECIMAL:
          self.value = int(value,16)
  def __index__(self):
    return self.value
  def __eq__(self, value: object) -> bool:
    return self.value == value
  def __ne__(self, value: object) -> bool:
    return self.value != value
  def __ge__(self, value: object) -> bool:
    return self.value >= value
  def __le__(self, value: object) -> bool:
    return self.value <= value
  def __gt__(self, value: object) -> bool:
    return self.value >  value
  def __lt__(self, value: object) -> bool:
    return self.value <  value

class VCDSample:
  def __init__(self,timestamp:int,value:str):
    self.timestamp = timestamp
    self.value = value

  @classmethod
  def from_tuple(classs,tuple:tuple[int,str]):
    return classs(tuple[0],tuple[1])

  def __tuple__(self):
    return (self.timestamp, self.value)

  def __repr__(self):
    return f"'{self.timestamp}ns:{self.value}'"

class SearchMethod(Enum):
  WALKING = 0
  BINARY  = 1
  SMART   = 2

class EdgePolarity(Enum):
  RISING  = 0
  FALLING = 1

class TimeDirection(Enum):
  NEXT     = 0
  PREVIOUS = 1

class VCDSignal:
  def __init__(self, vcd:list[VCDSample]):
    self.vcd            = vcd
    self.current_sample = vcd[0]
    self.current_index  = 0
    self.finished       = False

  def get_at_timestamp(self, timestamp:int, move:bool=False) -> VCDSample:
    search_index  = bisect_right(self.vcd, timestamp, lo=self.current_sample.timestamp, key=lambda x:x.timestamp)-1
    search_sample = self.vcd[search_index]
    if move:
      self.current_index  = search_index
      self.current_sample = search_sample
    return search_sample

  def get_edge(self, polarity:EdgePolarity=EdgePolarity.RISING, direction:TimeDirection=TimeDirection.NEXT, move:bool=False) -> VCDSample:
    search_index = self.current_index
    while True:
      if direction == TimeDirection.NEXT:
        search_index += 1
      else:
        search_index -= 1
      if search_index == 0 or search_index == len(self.vcd):
        if move:
          self.current_index  = search_index
          self.current_sample = search_sample
          if direction == TimeDirection.NEXT:
            self.finished = True
        return None
      search_sample = self.vcd[search_index]
      if search_sample.value == "1":
        if move:
          self.current_index  = search_index
          self.current_sample = search_sample
        return search_sample

  def get_edge_at_timestamp(self, timestamp:int, polarity:EdgePolarity=EdgePolarity.RISING, direction:TimeDirection=TimeDirection.NEXT, exclusive:bool=False, move:bool=False) -> VCDSample:
    search_sample = self.get_at_timestamp(timestamp, move=move)
    if not (    ( search_sample.timestamp == timestamp )
            and (  ( polarity == EdgePolarity.RISING  and search_sample.value == "1" )
                or ( polarity == EdgePolarity.FALLING and search_sample.value == "0" ) ) ):
      search_sample = self.get_edge(polarity, direction, move=move)
    return search_sample

class VCDFile:
  def __init__(self, vcd_path:str):
    vcd = VcdParser()
    with open(vcd_path) as vcd_file:
      vcd.parse(vcd_file)
    self.vcd = vcd.scope

  def get_signal(self, path:list[str], scope:VcdVarScope=None):
    if scope is None:
      scope = self.vcd
    if not path:
      return VCDSignal([VCDSample(vcd_tuple[0],vcd_tuple[1]) for vcd_tuple in scope.data])
    else:
      return self.get_signal(path[1:], scope.children[path[0]])
