from enum import Enum
from bisect import bisect_right
from pyDigitalWaveTools.vcd.parser import VcdParser, VcdVarScope






class VCDFormat(Enum):
  """ Number format of VCD values. """
  BINARY = 0
  REAL   = 1




class VCDValue:
  """ Represent a value from a VCD with useful methods. """



  def __init__(self, value:str, width:int):
    """ VCD value from the raw values from the VCD and the width of the signal. """

    self.width = width

    # Single character means a 1-bit signal
    if width == 1:
      self.format = VCDFormat.BINARY
      self.value = value[-1]

    # Multiple characters can be a real or multi-bit binary number
    else:

      # Separate the identifier code and the actual value
      identifier_code = value[0]
      value           = value[1:]

      # Real number
      if identifier_code == 'r' or identifier_code == 'R':
        self.format = VCDFormat.REAL
        self.value  = value

      # Binary number
      elif identifier_code == 'b' or identifier_code == 'B':
        self.format = VCDFormat.BINARY

        # Pad the binary number to the width of the signal
        if len(value) < width:

          # If the MSB is 1, then pad with 0
          if value[0] == '1':
            value = value.rjust(width, '0')

          # Else pad with the last character (0, X or Z)
          else:
            value = value.rjust(width, value[0])

        # Store the formatted value
        self.value = value

    # Flag to easily identify values not fully defined
    self.has_xz = 'x' in self.value or 'X' in self.value or 'z' in self.value or 'Z' in value



  def __getitem__(self, key):
    """ The [] operator uses binary indexing instead of string indexing. """
    value_sliced = self.value[::-1][key]
    return VCDValue(value_sliced, len(value_sliced))



  def decimal(self) -> int|None:
    """ Returns the decimal representation of the value. """

    # Real values are already stored as decimal
    if self.format == VCDFormat.REAL:
      return self.value

    # If there are X or Z, return None
    if self.has_xz:
      return None

    # Else use the Python bin to int function
    return int(self.value, 2)



  def hexadecimal(self):
    """ Returns the hexadecimal representation of the value. """

    # For real values, use the Python hex function
    if self.format == VCDFormat.REAL:
      return hex(self.value)[2:]

    # Building the result nibble by nibble
    value_hex = ""
    value_bin = self.value
    while value_bin:
      nibble_hex = "?"
      nibble_bin = value_bin[-4:]
      value_bin  = value_bin[:-4]

      # Count the number of 0, 1, X, Z
      count_0 = nibble_bin.count('0')
      count_1 = nibble_bin.count('1')
      count_x = nibble_bin.count('x') + nibble_bin.count('X')
      count_z = nibble_bin.count('z') + nibble_bin.count('Z')

      # If there are 0s or 1s
      if count_0 or count_1:

        # If there are Xs or Zs
        if   count_x: nibble_hex = "X"
        elif count_z: nibble_hex = "Z"

        # Else normal bin to hex
        else:
          nibble_bin = nibble_bin.rjust(4,'0')
          match nibble_bin:
            case '0000': nibble_hex = '0'
            case '0001': nibble_hex = '1'
            case '0010': nibble_hex = '2'
            case '0011': nibble_hex = '3'
            case '0100': nibble_hex = '4'
            case '0101': nibble_hex = '5'
            case '0110': nibble_hex = '6'
            case '0111': nibble_hex = '7'
            case '1000': nibble_hex = '8'
            case '1001': nibble_hex = '9'
            case '1010': nibble_hex = 'A'
            case '1011': nibble_hex = 'B'
            case '1100': nibble_hex = 'C'
            case '1101': nibble_hex = 'D'
            case '1110': nibble_hex = 'E'
            case '1111': nibble_hex = 'F'

      # Else if only Xs or Zs
      elif count_x: nibble_hex = "x"
      elif count_z: nibble_hex = "z"

      # Append to result string
      value_hex = nibble_hex + value_hex

    return value_hex



  def __repr__(self):
    """ Convert to string with the hexadecimal representation. """
    return self.hexadecimal()



  def __eq__(self, value: object) -> bool:
    """ Compare two VCDValues with the raw values, else compare using the hexadecimal representation. """
    if isinstance(value, VCDValue):
      return self.value == value.value
    else:
      return self.__repr__() == str(value)



  def __ne__(self, value: object) -> bool:
    """ Compare two VCDValues with the raw values, else compare using the hexadecimal representation. """
    if isinstance(value, VCDValue):
      return self.value != value.value
    else:
      return self.__repr__() != str(value)






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
