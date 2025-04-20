from __future__ import annotations
from enum import Enum
from bisect import bisect_right
from pyDigitalWaveTools.vcd.parser import (
  VcdParser,
  VcdVarScope,
)






class VCDFormat(Enum):
  """ Number format of VCD values. """
  BINARY = 0
  REAL   = 1



class VCDValue:
  """ A value from a VCD. """

  def __init__(self, value:str="", width:int=0):
    """ VCD value from the raw values from the VCD and the width of the signal. """

    self.width = width

    # Empty string means empty binary value
    if len(value) == 0:
      self.format = VCDFormat.BINARY
      self.value  = ""

    # Single character means a 1-bit signal
    elif width == 1 or len(value) == 1:
      self.format = VCDFormat.BINARY
      self.value  = value[-1]

    # Multiple characters can be a real or multi-bit binary number
    else:

      # Separate the identifier code and the actual value
      identifier_code = value[0]
      value           = value[1:]

      # Real number
      if identifier_code == 'r' or identifier_code == 'R':
        self.format = VCDFormat.REAL
        self.value  = int(value)

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
    self.has_xz = self.format == VCDFormat.BINARY and ('x' in self.value or 'X' in self.value or 'z' in self.value or 'Z' in value)


  def __getitem__(self, key:int|slice) -> VCDValue:
    """ The [] operator uses binary indexing instead of string indexing. """
    value_sliced = self.value[::-1][key][::-1]
    return VCDValue("b"+value_sliced, len(value_sliced))

  def __setitem__(self, key:int|slice, value:VCDValue) -> None:
    """ The [] operator uses binary indexing instead of string indexing. """
    value_modified      = list(self.value)        # String to list to use item assignment
    value_modified      = value_modified[::-1]    # Reverse to use binary indexing
    value_modified[key] = list(value.value)[::-1] # Assign item with reverse order
    value_modified      = value_modified[::-1]    # Reverse back the list
    value_modified      = ''.join(value_modified) # List to string
    self.value          = value_modified

  def __len__(self) -> int:
    """ Length is the width of the binary value. """
    return self.width

  def __pow__(self, other:VCDValue) -> VCDValue:
    """ Exponentiation overloaded for concatenation. """
    return VCDValue("b" + self.value + other.value, self.width + other.width)

  def __rshift__(self, other:int) -> VCDValue:
    """ Right shift. """
    if other >= self.width:
      return VCDValue("0", 1)
    else:
      return VCDValue("b" + self.value[other:], self.width - other)

  def __lshift__(self, other:int) -> VCDValue:
    """ Left shift. """
    return VCDValue("b" + self.value + other*"0", self.width + other)

  def __invert__(self) -> VCDValue:
    """ Binary inversion. """
    value_invert = ""
    for bit in self.value:
      value_invert += {'0':'1', '1':'0', 'x':'x', 'z':'z'} [bit]
    return VCDValue("b" + value_invert, self.width)


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



  def hexadecimal(self) -> str:
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



  def __repr__(self) -> str:
    """ Convert to string with the hexadecimal representation. """
    return self.hexadecimal()

  def __int__(self) -> int:
    """ Convert to integer. """
    return self.decimal()

  def __bool__(self) -> bool:
    """ Convert to boolean. True if at least one 1, false otherwise. """
    return '1' in self.__repr__()

  def __eq__(self, value:object) -> bool:
    """ Compare two VCDValues with the raw values, else compare using the hexadecimal representation. """
    if isinstance(value, VCDValue):
      return self.value == value.value
    else:
      return self.__repr__() == str(value)

  def __ne__(self, value:object) -> bool:
    """ Compare two VCDValues with the raw values, else compare using the hexadecimal representation. """
    if isinstance(value, VCDValue):
      return self.value != value.value
    else:
      return self.__repr__() != str(value)

  def equal_no_xy(self, other:VCDValue) -> bool:
    """ Equality comparison that interprets X and Z as don't care and only checks the LSBs up to the shortest value. """
    if self.format == VCDFormat.REAL: return self == other
    for self_bit, other_bit in zip(self.value, other.value):
      if self_bit != other_bit and self_bit not in 'xXzZ' and other_bit not in 'xXzZ':
        return False
    return True


  @classmethod
  def none(cls):
    """ Empty value. """
    return cls("",0)

  @classmethod
  def zero(cls):
    """ Single bit 0. """
    return cls("0",1)

  @classmethod
  def one(cls):
    """ Single bit 1. """
    return cls("1",1)

  @classmethod
  def x(cls):
    """ Single bit X. """
    return cls("x",1)

  @classmethod
  def z(cls):
    """ Single bit Z. """
    return cls("z",1)






class VCDSample:
  """ A sample from a VCD. """

  def __init__(self,timestamp:int,value:VCDValue):
    """ VCDSample from a timestamp and a VCDValue. """
    self.timestamp = timestamp
    self.value = value

  def __tuple__(self):
    """ Convert of tuple of timestamp and value. """
    return (self.timestamp, self.value)

  def __repr__(self):
    """ String representation with timestamp unit. """
    return f"'{self.timestamp}ns:{self.value}'"






class SearchMethod(Enum):
  """ Algorithm to search for a timestamp in a VCD. """
  WALKING = 0
  BINARY  = 1
  SMART   = 2

class EdgePolarity(Enum):
  """ Signal edge polarity. """
  RISING  = 0
  FALLING = 1
  ANY     = 2

class ComparisonOperation(Enum):
  """ Value comparison operation. """
  EQUAL_EXACT     = 0
  EQUAL_NO_XY     = 1
  NOT_EQUAL_EXACT = 2
  NOT_EQUAL_NO_XY = 3

class TimeDirection(Enum):
  """ Search for the next or previous edge. """
  NEXT     = 0
  PREVIOUS = 1



class VCDSignal:
  """ A signal of a VCD with its dump. """

  def __init__(self, vcd:list[VCDSample], width:int):
    """ VCDSignal from a list of VCDSamples and a width. """
    self.vcd               = vcd
    self.current_index     = 0
    self.current_sample    = vcd[self.current_index]
    self.current_timestamp = self.current_sample.timestamp
    self.finished          = False
    self.width             = width



  def get_at_timestamp(self, timestamp:int, move:bool=False) -> VCDSample:
    """ Get the last sample at or before a timestamp. """

    # Use binary search
    search_index  = bisect_right(self.vcd, timestamp, key=lambda x:x.timestamp)-1
    search_sample = self.vcd[search_index]

    # Update the state of the signal
    if move:
      self.current_index     = search_index
      self.current_sample    = search_sample
      self.current_timestamp = timestamp
    return search_sample



  def get_edge(self,
               polarity   : EdgePolarity        = EdgePolarity.RISING,
               value      : VCDValue            = None,
               comparison : ComparisonOperation = ComparisonOperation.EQUAL_NO_XY,
               direction  : TimeDirection       = TimeDirection.NEXT,
               move       : bool                = False,
               ) -> VCDSample:
    """ Get an edge by polarity or value from the current timestamp. """

    # If we already reached the end, there is no next edge
    if direction == TimeDirection.NEXT and self.finished:
      return None

    # Iterate over the indices from the current one in the selected direction
    search_index = self.current_index
    while True:

      # Move to next or previous edge
      if direction == TimeDirection.NEXT:
        search_index += 1
      else:
        search_index -= 1

      # If we reached the start or end of the dump
      if search_index == 0 or search_index == len(self.vcd):

        # Update the state of the signal
        if move:
          self.current_index = search_index
          if search_index == len(self.vcd):
            self.current_sample = self.vcd[-1]
          else: self.current_sample = self.vcd[search_index]
          self.current_timestamp = self.current_sample.timestamp

          # Update the finished flag at the end of the dump
          if direction == TimeDirection.NEXT:
            self.finished = True

        # Return None if no matching edge found
        return None

      # Check the search condition of the edge
      search_sample = self.vcd[search_index]
      search_match  = False

      # Search by value
      if value is not None:
        if comparison == ComparisonOperation.EQUAL_EXACT:
          search_match = search_sample.value == value
        elif comparison == ComparisonOperation.EQUAL_NO_XY:
          search_match = search_sample.value.equal_no_xy(value)
        elif comparison == ComparisonOperation.NOT_EQUAL_EXACT:
          search_match = search_sample.value != value
        elif comparison == ComparisonOperation.NOT_EQUAL_NO_XY:
          search_match = not search_sample.value.equal_no_xy(value)

      # Search by edge polarity
      else:
        search_match = (   (polarity == EdgePolarity.RISING  and search_sample.value == 1)
                        or (polarity == EdgePolarity.FALLING and search_sample.value == 0)
                        or (polarity == EdgePolarity.ANY) )

      # If the search condition matches
      if search_match:

        # Update the state of the signal
        if move:
          self.current_index  = search_index
          self.current_sample = search_sample
          self.current_timestamp = self.current_sample.timestamp

        # Return the matching edge
        return search_sample



  def get_edge_at_timestamp(self,
                            timestamp          : int,
                            polarity           : EdgePolarity  = EdgePolarity.RISING,
                            direction          : TimeDirection = TimeDirection.NEXT,
                            match_on_timestamp : bool          = True,
                            move               : bool          = False,
                            ) -> VCDSample:
    """ Get the next or previous rising or falling edge from a timestamp. """

    # If don't move, then backup the current state
    if not move:
      backup_current_index     = self.current_index
      backup_current_sample    = self.current_sample
      backup_current_timestamp = self.current_timestamp
      backup_finished          = self.finished

    # First move to the last edge at or before the timestamp
    search_sample = self.get_at_timestamp(timestamp, move=True)

    # If we land on a matching edge, return it
    if (    match_on_timestamp
        and ( search_sample.timestamp == timestamp )
        and (  ( polarity == EdgePolarity.RISING  and search_sample.value == 1 )
            or ( polarity == EdgePolarity.FALLING and search_sample.value == 0 )
            or ( polarity == EdgePolarity.ANY ) ) ):
      pass

    # Else get the edge from there
    else:
      search_sample = self.get_edge(polarity=polarity, direction=direction, move=True)

    # If don't move, then restore the backup state
    if not move:
      self.current_index     = backup_current_index
      self.current_sample    = backup_current_sample
      self.current_timestamp = backup_current_timestamp
      self.finished          = backup_finished

    return search_sample



def get_value_at_timestamp_if_signal_exists(signal  : VCDSignal|None,
                                            default : VCDValue|None = None,
                                            **kwargs
                                            ) -> VCDValue|None:
  """ Get the value of the last sample at or before a timestamp if the signal exists (is not None), else it returns a default value (None by default). """
  if signal is None:
    return default
  else:
    sample = signal.get_at_timestamp(**kwargs)
    if sample is not None:
      return sample.value
    else:
      return default



def get_value_of_edge_if_signal_exists(signal  : VCDSignal|None,
                                       default : VCDValue|None = None,
                                       **kwargs
                                       ) -> VCDValue|None:
  """ Get the value of an edge by polarity or value from the current timestamp if the signal exists (is not None), else it returns a default value (None by default). """
  if signal is None:
    return default
  else:
    sample = signal.get_edge(**kwargs)
    if sample is not None:
      return sample.value
    else:
      return default



def get_value_of_edge_at_timestamp_if_signal_exists(signal  : VCDSignal|None,
                                                    default : VCDValue|None = None,
                                                    **kwargs
                                                    ) -> VCDValue|None:
  """ Get the value of the next or previous rising or falling edge from a timestamp if the signal exists (is not None), else it returns a default value (None by default). """
  if signal is None:
    return default
  else:
    sample = signal.get_edge_at_timestamp(**kwargs)
    if sample is not None:
      return sample.value
    else:
      return default



def get_next_valid_ready_handshake_timestamp(clock : VCDSignal,
                                             valid : VCDSignal,
                                             ready : VCDSignal,
                                             ) -> int|None:
  """ Get the timestamp of the next valid-ready handshake. This moves the pointers for all three signals. Returns None if no handshake were found. """

  # First we check the next cycle after the last sample of the ready signal.
  # If the valid is high, then we fetch the timestamp of the handshake.
  # Else we go to the next rising edge of the valid.
  # We do this instead of checking the next valid edge directly because for
  # back-to-back packets, the valid stays high after the first handshake
  # without an edge.

  # Move back the clock to the last ready timestamp
  last_ready_timestamp = ready.current_timestamp
  clock.get_edge_at_timestamp(last_ready_timestamp, move=True)

  # Next clock cycle
  clock_sample = clock.get_edge(move=True)
  if clock_sample is None: return None
  clock_timestamp = clock_sample.timestamp

  # Sample the valid signal (at the cycle after the previous ready)
  valid_sample = valid.get_at_timestamp(clock_timestamp, move=True)
  if valid_sample is None: return None
  valid_value = valid_sample.value
  if valid_value:
    valid_timestamp = clock_timestamp

  # If valid is low, then sample the next valid rising edge
  else:
    valid_sample = valid.get_edge(move=True)
    if valid_sample is None: return None
    valid_timestamp = valid_sample.timestamp

  # Sample the ready (check if already high, else get rising edge)
  ready_sample = ready.get_at_timestamp(valid_timestamp, move=True)
  ready_value = ready_sample.value
  if ready_value:
    ready_timestamp = valid_timestamp
  else:
    ready_sample = ready.get_edge_at_timestamp(valid_timestamp, move=True)
    if ready_sample is None: return None
    ready_timestamp = ready_sample.timestamp

  # Get the rising edge of the clock
  clock_sample = clock.get_edge_at_timestamp(ready_timestamp, move=True)
  if clock_sample is None: return None
  timestamp_clock = clock_sample.timestamp

  return timestamp_clock






class VCDFile:
  """ A wrapper around pyDigitalWaveTools.VcdParser for a VCD file. """

  def __init__(self, vcd_path:str):
    """ Parse the VCD from the file. """
    vcd = VcdParser()
    with open(vcd_path) as vcd_file:
      vcd.parse(vcd_file)
    self.vcd = vcd.scope

  def get_signal(self, path:list[str], scope:VcdVarScope=None) -> VCDSignal:
    """ Get a VCDSignal from the VCD recursively. """

    # Initialize the recursion at the root of the dump scope
    if scope is None:
      scope = self.vcd

    # If the path is empty, the scope is the signal, end of recursion
    if not path:

      # Build the list of samples
      vcd_samples = []
      signal_width = scope.width
      for sample_tuple in scope.data:
        sample_timestamp = sample_tuple[0]
        sample_value     = VCDValue(sample_tuple[1], signal_width)
        vcd_sample       = VCDSample(sample_timestamp, sample_value)
        vcd_samples.append(vcd_sample)

      # Return the VCDSignal
      vcd_signal = VCDSignal(vcd_samples, signal_width)
      return vcd_signal

    # Else continue recursion
    else:

      # Check if searched path or signal exists to continue
      if path[0] in scope.children:
        return self.get_signal(path[1:], scope.children[path[0]])

      # Return None if path or signal doesn't exist
      else:
        return None
