from enum import Enum
from bisect import bisect_right
from pyDigitalWaveTools.vcd.parser import VcdParser, VcdVarScope



class VCDFormat(Enum):
  BINARY = 0
  REAL   = 1

class VCDValue:
  def __init__(self, value:str, width:int):
    self.width = width
    if width == 1:
      self.value = value[-1]
    else:
      if len(value) > 1:
        identifier_code = value[0]
        value = value[1:]
        if identifier_code == 'r' or identifier_code == 'R':
          self.format = VCDFormat.REAL
          self.value = value
        elif identifier_code == 'b' or identifier_code == 'B':
          self.format = VCDFormat.BINARY
          if len(value) < width:
            if value[0] == '1':
              value = value.rjust(width, '0')
            else:
              value = value.rjust(width, value[0])
          self.value = value
    value_no_xz = self.value.replace('x','0').replace('X','0').replace('z','0').replace('Z','0')
    self.has_xz = self.value != value_no_xz

  def __getitem__(self, key):
    value_sliced = self.value[::-1][key]
    return VCDValue(value_sliced, len(value_sliced))

  def __repr__(self):
    return self.value
  def __index__(self):
    return self.value

  def __eq__(self, value: object) -> bool:
    return self.value == str(value)
  def __ne__(self, value: object) -> bool:
    return self.value != str(value)
  def __ge__(self, value: object) -> bool:
    return self.value >= str(value)
  def __le__(self, value: object) -> bool:
    return self.value <= str(value)
  def __gt__(self, value: object) -> bool:
    return self.value >  str(value)
  def __lt__(self, value: object) -> bool:
    return self.value <  str(value)



class VCDSample:
  def __init__(self,timestamp:int,value:VCDValue):
    self.timestamp = timestamp
    self.value = value

  @classmethod
  def from_tuple(classs,tuple:tuple[int,VCDValue]):
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
  def __init__(self, vcd:list[VCDSample], width:int):
    self.vcd            = vcd
    self.current_sample = vcd[0]
    self.current_index  = 0
    self.finished       = False
    self.width          = width

  def get_at_timestamp(self, timestamp:int, move:bool=False) -> VCDSample:
    search_index  = bisect_right(self.vcd, timestamp, lo=self.current_index, key=lambda x:x.timestamp)-1
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
      if search_sample.value == 1:
        if move:
          self.current_index  = search_index
          self.current_sample = search_sample
        return search_sample

  def get_edge_at_timestamp(self, timestamp:int, polarity:EdgePolarity=EdgePolarity.RISING, direction:TimeDirection=TimeDirection.NEXT, exclusive:bool=False, move:bool=False) -> VCDSample:
    search_sample = self.get_at_timestamp(timestamp, move=move)
    if not (    ( search_sample.timestamp == timestamp )
            and (  ( polarity == EdgePolarity.RISING  and search_sample.value == 1 )
                or ( polarity == EdgePolarity.FALLING and search_sample.value == 0 ) ) ):
      search_sample = self.get_edge(polarity, direction, move=move)
    return search_sample



class VCDFile:
  def __init__(self, vcd_path:str):
    vcd = VcdParser()
    with open(vcd_path) as vcd_file:
      vcd.parse(vcd_file)
    self.vcd = vcd.scope

  def get_signal(self, path:list[str], scope:VcdVarScope=None) -> VCDSignal:
    if scope is None:
      scope = self.vcd
    if not path:
      vcd_samples = []
      signal_width = scope.width
      for sample_tuple in scope.data:
        sample_timestamp = sample_tuple[0]
        sample_value     = VCDValue(sample_tuple[1], signal_width)
        vcd_sample       = VCDSample(sample_timestamp, sample_value)
        vcd_samples.append(vcd_sample)
      vcd_signal = VCDSignal(vcd_samples, signal_width)
      return vcd_signal
    else:
      if path[0] in scope.children:
        return self.get_signal(path[1:], scope.children[path[0]])
      else:
        return None
