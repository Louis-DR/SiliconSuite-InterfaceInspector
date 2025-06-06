from dataclasses import dataclass
from enum        import Enum
from typing      import Generator

from .vcd import (
  VCDFile,
  VCDValue,
  ComparisonOperation,
  EdgePolarity,
)

from .utils import (
  change_case,
  packet_string,
  Color,
  remove_colors,
)

from .packet    import Packet
from .interface import Interface
from .annotator import Annotator






command_width = 5
context_width = 0
value_width   = 2
line_width    = 50

write_latency  = 10
read_latency   = 35
burst_length   = 4
data_bus_width = 64
data_width     = data_bus_width * burst_length

enable_data_bus_inversion = True
class HBM2eCommand(Packet):
  """ HBM2e command base type. """

class HBM2eRowCommand(HBM2eCommand):
  """ HBM2e row command base type. """

class HBM2eRowCommand_Error(HBM2eRowCommand):
  """ HBM2e incorrect row command. """
  def __init__(self, timestamp:int):
    self.timestamp = timestamp
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "ERROR",
      parameters = {},
      context    = "R",
      color      = Color.BG_BLACK + Color.RED + Color.BLINK,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eRowCommand_Activate(HBM2eRowCommand):
  """ HBM2e activate row command. """
  def __init__(self,
               timestamp      : int,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue,
               row_address    : VCDValue):
    self.timestamp      = timestamp
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
    self.row_address    = row_address
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "ACT",
      parameters = {"PS":  self.pseudo_channel .decimal(),
                    "SID": self.stack_id       .decimal(),
                    "BA":  self.bank_address   .decimal(),
                    "RA":  self.row_address    .decimal()},
      context    = "R",
      color      = Color.BG_RED,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eRowCommand_Precharge(HBM2eRowCommand):
  """ HBM2e precharge row command. """
  def __init__(self,
               timestamp      : int,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue):
    self.timestamp      = timestamp
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "PRE",
      parameters = {"PS":  self.pseudo_channel .decimal(),
                    "SID": self.stack_id       .decimal(),
                    "BA":  self.bank_address   .decimal()},
      context    = "R",
      color      = Color.BG_GREEN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eRowCommand_PrechargeAll(HBM2eRowCommand):
  """ HBM2e precharge-all row command. """
  def __init__(self,
               timestamp      : int,
               parity         : VCDValue,
               pseudo_channel : VCDValue):
    self.timestamp      = timestamp
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "PREA",
      parameters = {"PS": self.pseudo_channel.decimal()},
      context    = "R",
      color      = Color.BG_GREEN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eRowCommand_SingleBankRefresh(HBM2eRowCommand):
  """ HBM2e single-bank refresh row command. """
  def __init__(self,
               timestamp      : int,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue):
    self.timestamp      = timestamp
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "REFSB",
      parameters = {"PS":  self.pseudo_channel .decimal(),
                    "SID": self.stack_id       .decimal(),
                    "BA":  self.bank_address   .decimal()},
      context    = "R",
      color      = Color.BG_BLUE,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eRowCommand_Refresh(HBM2eRowCommand):
  """ HBM2e refresh row command. """
  def __init__(self,
               timestamp      : int,
               parity         : VCDValue,
               pseudo_channel : VCDValue):
    self.timestamp      = timestamp
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "REF",
      parameters = {"PS": self.pseudo_channel.decimal()},
      context    = "R",
      color      = Color.BG_BLUE,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eRowCommand_PowerDownEntry(HBM2eRowCommand):
  """ HBM2e power-down entry row command. """
  def __init__(self,
               timestamp : int,
               parity    : VCDValue):
    self.timestamp = timestamp
    self.parity    = parity
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "PDE",
      parameters = {},
      context    = "R",
      color      = Color.BG_WHITE + Color.BLACK,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eRowCommand_SelfRefreshEntry(HBM2eRowCommand):
  """ HBM2e self-refresh entry row command. """
  def __init__(self,
               timestamp : int,
               parity    : VCDValue):
    self.timestamp = timestamp
    self.parity    = parity
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "SRE",
      parameters = {},
      context    = "R",
      color      = Color.BG_WHITE + Color.BLACK,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eRowCommand_PowerDownSelfRefreshExit(HBM2eRowCommand):
  """ HBM2e power-down or self-refresh exit row command. """
  def __init__(self, timestamp:int):
    self.timestamp = timestamp
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "PDX/SRX",
      parameters = {},
      context    = "R",
      color      = Color.BG_WHITE + Color.BLACK,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )






class HBM2eColumnCommand(HBM2eCommand):
  """ HBM2e column command base type. """
  pass

class HBM2eColumnCommand_Error(HBM2eColumnCommand):
  """ HBM2e incorrect column command. """
  def __init__(self, timestamp:int):
    self.timestamp = timestamp
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "ERROR",
      parameters = {},
      context    = "C",
      color      = Color.BG_BLACK + Color.RED + Color.BLINK,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eColumnCommand_Read(HBM2eColumnCommand):
  """ HBM2e read column command. """
  def __init__(self,
               timestamp      : int,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue,
               column_address : VCDValue):
    self.timestamp      = timestamp
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
    self.column_address = column_address
    self.data           = None
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "RD",
      parameters = {"PS":  self.pseudo_channel .decimal(),
                    "SID": self.stack_id       .decimal(),
                    "BA":  self.bank_address   .decimal(),
                    "CA":  self.column_address .decimal()},
      context    = "C",
      color      = Color.BG_YELLOW,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eColumnCommand_ReadAutoPrecharge(HBM2eColumnCommand):
  """ HBM2e read with auto-precharge column command. """
  def __init__(self,
               timestamp      : int,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue,
               column_address : VCDValue):
    self.timestamp      = timestamp
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
    self.column_address = column_address
    self.data           = None
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "RDA",
      parameters = {"PS":  self.pseudo_channel .decimal(),
                    "SID": self.stack_id       .decimal(),
                    "BA":  self.bank_address   .decimal(),
                    "CA":  self.column_address .decimal()},
      context    = "C",
      color      = Color.BG_YELLOW,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eColumnCommand_Write(HBM2eColumnCommand):
  """ HBM2e write column command. """
  def __init__(self,
               timestamp      : int,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue,
               column_address : VCDValue):
    self.timestamp      = timestamp
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
    self.column_address = column_address
    self.data           = None
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "WR",
      parameters = {"PS":  self.pseudo_channel .decimal(),
                    "SID": self.stack_id       .decimal(),
                    "BA":  self.bank_address   .decimal(),
                    "CA":  self.column_address .decimal()},
      context    = "C",
      color      = Color.BG_CYAN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eColumnCommand_WriteAutoPrecharge(HBM2eColumnCommand):
  """ HBM2e write with auto-precharge column command. """
  def __init__(self,
               timestamp      : int,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue,
               column_address : VCDValue):
    self.timestamp      = timestamp
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
    self.column_address = column_address
    self.data           = None
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "WRA",
      parameters = {"PS":  self.pseudo_channel .decimal(),
                    "SID": self.stack_id       .decimal(),
                    "BA":  self.bank_address   .decimal(),
                    "CA":  self.column_address .decimal()},
      context    = "C",
      color      = Color.BG_CYAN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class HBM2eColumnCommand_ModeRegisterSet(HBM2eColumnCommand):
  """ HBM2e mode register set column command. """
  def __init__(self,
               timestamp     : int,
               parity        : VCDValue,
               mode_register : VCDValue,
               operation     : VCDValue):
    self.timestamp     = timestamp
    self.parity        = parity
    self.mode_register = mode_register
    self.operation     = operation
  def __repr__(self):
    return packet_string(
      timestamp  = self.timestamp,
      command    = "MRS",
      parameters = {"MR": self.mode_register .decimal(),
                    "OP": self.operation     .decimal()},
      context    = "C",
      color      = Color.BG_MAGENTA,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )






@dataclass
class HBM2eInterfacePaths:
  """ A set of HBM2e signal paths. """
  CK_T   : str = "CK_T"
  CK_C   : str = "CK_C"
  CKE    : str = "CKE"
  R      : str = "R"
  C      : str = "C"
  RDQS_T : str = "RDQS_T"
  RDQS_C : str = "RDQS_C"
  WDQS_T : str = "WDQS_T"
  WDQS_C : str = "WDQS_C"
  DQ     : str = "DQ"
  DBI    : str = "DBI"
  DM     : str = "DM"
  PAR    : str = "PAR"
  DERR   : str = "DERR"
  AERR   : str = "AERR"

class HBM2eInterface(Interface):
  """ An HBM2e interface with its VCD signals. """

  def __init__(self,
               vcd_file  : VCDFile,
               signals   : HBM2eInterfacePaths = None,
               path      : str                 = "",
               prefix    : str                 = "",
               suffix    : str                 = "",
               uppercase : bool                = True):
    """ Get all the signals of the HBM2e bus. """
    if signals is None:
      self.paths = HBM2eInterfacePaths()
      self.paths.CK_T   = f"{path}.{prefix}{change_case('CK_T',   uppercase)}{suffix}"
      self.paths.CK_C   = f"{path}.{prefix}{change_case('CK_C',   uppercase)}{suffix}"
      self.paths.CKE    = f"{path}.{prefix}{change_case('CKE',    uppercase)}{suffix}"
      self.paths.R      = f"{path}.{prefix}{change_case('R',      uppercase)}{suffix}"
      self.paths.C      = f"{path}.{prefix}{change_case('C',      uppercase)}{suffix}"
      self.paths.RDQS_T = f"{path}.{prefix}{change_case('RDQS_T', uppercase)}{suffix}"
      self.paths.RDQS_C = f"{path}.{prefix}{change_case('RDQS_C', uppercase)}{suffix}"
      self.paths.WDQS_T = f"{path}.{prefix}{change_case('WDQS_T', uppercase)}{suffix}"
      self.paths.WDQS_C = f"{path}.{prefix}{change_case('WDQS_C', uppercase)}{suffix}"
      self.paths.DQ     = f"{path}.{prefix}{change_case('DQ',     uppercase)}{suffix}"
      self.paths.DBI    = f"{path}.{prefix}{change_case('DBI',    uppercase)}{suffix}"
      self.paths.DM     = f"{path}.{prefix}{change_case('DM',     uppercase)}{suffix}"
      self.paths.PAR    = f"{path}.{prefix}{change_case('PAR',    uppercase)}{suffix}"
      self.paths.DERR   = f"{path}.{prefix}{change_case('DERR',   uppercase)}{suffix}"
      self.paths.AERR   = f"{path}.{prefix}{change_case('AERR',   uppercase)}{suffix}"
    else: self.paths = signals
    self.CK_T   = vcd_file.get_signal( self.paths.CK_T   .split('.') )
    self.CK_C   = vcd_file.get_signal( self.paths.CK_C   .split('.') )
    self.CKE    = vcd_file.get_signal( self.paths.CKE    .split('.') )
    self.R      = vcd_file.get_signal( self.paths.R      .split('.') )
    self.C      = vcd_file.get_signal( self.paths.C      .split('.') )
    self.RDQS_T = vcd_file.get_signal( self.paths.RDQS_T .split('.') )
    self.RDQS_C = vcd_file.get_signal( self.paths.RDQS_C .split('.') )
    self.WDQS_T = vcd_file.get_signal( self.paths.WDQS_T .split('.') )
    self.WDQS_C = vcd_file.get_signal( self.paths.WDQS_C .split('.') )
    self.DQ     = vcd_file.get_signal( self.paths.DQ     .split('.') )
    self.DBI    = vcd_file.get_signal( self.paths.DBI    .split('.') )
    self.DM     = vcd_file.get_signal( self.paths.DM     .split('.') )
    self.PAR    = vcd_file.get_signal( self.paths.PAR    .split('.') )
    self.DERR   = vcd_file.get_signal( self.paths.DERR   .split('.') )
    self.AERR   = vcd_file.get_signal( self.paths.AERR   .split('.') )



  def next_row_command(self) -> HBM2eRowCommand:
    """ Get the next HBM2e row command. """

    # Get the next non-NOP row command
    sample_R = self.R.get_edge(value=VCDValue("bxxxx111",7), comparison=ComparisonOperation.NOT_EQUAL_NO_XY, move=True)
    if sample_R is None: return None

    # First word of the row command
    timestamp_row_command_w0 = self.CK_T.get_edge_at_timestamp(sample_R.timestamp, polarity=EdgePolarity.RISING, move=True).timestamp
    row_command_w0 = self.R.get_at_timestamp(timestamp_row_command_w0, move=True).value
    row_command_cke = self.CKE.get_at_timestamp(timestamp_row_command_w0, move=True).value

    # Second word of the row command
    timestamp_row_command_w1 = self.CK_T.get_edge(polarity=EdgePolarity.FALLING, move=True).timestamp
    row_command_w1 = self.R.get_at_timestamp(timestamp_row_command_w1, move=True).value

    # Decode the row command function using the truth table
    row_command_function = HBM2eRowCommand_Error
    if   row_command_w0.equal_no_xy(VCDValue("bxxxxx10",7)):                                                        row_command_function = HBM2eRowCommand_Activate
    elif row_command_w0.equal_no_xy(VCDValue("bxxxx011",7)) and row_command_w1.equal_no_xy(VCDValue("bxx0xxxx",7)): row_command_function = HBM2eRowCommand_Precharge
    elif row_command_w0.equal_no_xy(VCDValue("bxxxx011",7)) and row_command_w1.equal_no_xy(VCDValue("bxx1xxxx",7)): row_command_function = HBM2eRowCommand_PrechargeAll
    elif row_command_w0.equal_no_xy(VCDValue("bxxxx100",7)) and row_command_w1.equal_no_xy(VCDValue("bxx0xxxx",7)): row_command_function = HBM2eRowCommand_SingleBankRefresh
    elif row_command_w0.equal_no_xy(VCDValue("bxxxx100",7)) and row_command_w1.equal_no_xy(VCDValue("bxx1xxxx",7)): row_command_function = HBM2eRowCommand_Refresh
    elif row_command_w0.equal_no_xy(VCDValue("bxxxx111",7)) and row_command_cke == VCDValue("b0",0):                row_command_function = HBM2eRowCommand_PowerDownEntry
    elif row_command_w0.equal_no_xy(VCDValue("bxxxx100",7)) and row_command_cke == VCDValue("b0",0):                row_command_function = HBM2eRowCommand_SelfRefreshEntry

    # Activate command takes two cycles
    if row_command_function == HBM2eRowCommand_Activate:

      # Third word of the row command
      timestamp_row_command_w2 = self.CK_T.get_edge(polarity=EdgePolarity.RISING, move=True).timestamp
      row_command_w2 = self.R.get_at_timestamp(timestamp_row_command_w2, move=True).value

      # Fourth word of the row command
      timestamp_row_command_w3 = self.CK_T.get_edge(polarity=EdgePolarity.FALLING, move=True).timestamp
      row_command_w3 = self.R.get_at_timestamp(timestamp_row_command_w3, move=True).value

    # Decode the operands of the function
    row_command = HBM2eRowCommand_Error(timestamp = timestamp_row_command_w0)
    if row_command_function == HBM2eRowCommand_Activate:
      parity         = (   row_command_w3[2]
                        ** row_command_w1[2] )
      pseudo_channel =     row_command_w1[3]
      stack_id       = (   row_command_w1[6]
                        ** row_command_w0[2] )
      bank_address   = (   row_command_w1[5]
                        ** row_command_w0[3:6] )
      row_address    = (   row_command_w0[6]
                        ** row_command_w1[4]
                        ** row_command_w1[0:2]
                        ** row_command_w2[0:6]
                        ** row_command_w3[3:6]
                        ** row_command_w3[0:2] )
      row_command = HBM2eRowCommand_Activate (
        timestamp      = timestamp_row_command_w2,
        parity         = parity,
        pseudo_channel = pseudo_channel,
        stack_id       = stack_id,
        bank_address   = bank_address,
        row_address    = row_address,
      )
    elif row_command_function == HBM2eRowCommand_Precharge:
      parity         =     row_command_w1[2]
      pseudo_channel =     row_command_w1[3]
      stack_id       = (   row_command_w0[6]
                        ** row_command_w1[1] )
      bank_address   = (   row_command_w1[5]
                        ** row_command_w0[3:6] )
      row_command = HBM2eRowCommand_Precharge (
        timestamp      = timestamp_row_command_w0,
        parity         = parity,
        pseudo_channel = pseudo_channel,
        stack_id       = stack_id,
        bank_address   = bank_address,
      )
    elif row_command_function == HBM2eRowCommand_PrechargeAll:
      parity         =     row_command_w1[2]
      pseudo_channel =     row_command_w1[3]
      row_command = HBM2eRowCommand_PrechargeAll (
        timestamp      = timestamp_row_command_w0,
        parity         = parity,
        pseudo_channel = pseudo_channel,
      )
    elif row_command_function == HBM2eRowCommand_SingleBankRefresh:
      parity         =     row_command_w1[2]
      pseudo_channel =     row_command_w1[3]
      stack_id       = (   row_command_w0[6]
                        ** row_command_w1[1] )
      bank_address   = (   row_command_w1[5]
                        ** row_command_w0[3:6] )
      row_command = HBM2eRowCommand_SingleBankRefresh (
        timestamp      = timestamp_row_command_w0,
        parity         = parity,
        pseudo_channel = pseudo_channel,
        stack_id       = stack_id,
        bank_address   = bank_address,
      )
    elif row_command_function == HBM2eRowCommand_Refresh:
      parity         = row_command_w1[2]
      pseudo_channel = row_command_w1[3]
      row_command = HBM2eRowCommand_Refresh (
        timestamp      = timestamp_row_command_w0,
        parity         = parity,
        pseudo_channel = pseudo_channel,
      )
    elif row_command_function == HBM2eRowCommand_PowerDownEntry:
      parity = row_command_w1[2]
      row_command = HBM2eRowCommand_PowerDownEntry (
        timestamp = timestamp_row_command_w0,
        parity = parity,
      )
    elif row_command_function == HBM2eRowCommand_SelfRefreshEntry:
      parity = row_command_w1[2]
      row_command = HBM2eRowCommand_SelfRefreshEntry (
        timestamp = timestamp_row_command_w0,
        parity = parity,
      )

    return row_command



  def row_commands(self) -> Generator[HBM2eRowCommand, None, None]:
    """ Generator to iterate over all row commands. """
    while True:
      try:
        next_row_command = self.next_row_command()
        if next_row_command:
          yield next_row_command
        else: return
      except: return



  def next_column_command(self) -> HBM2eColumnCommand:
    """ Get the next HBM2e column command. """

    # Get the next non-NOP column command
    sample_C = self.C.get_edge(value=VCDValue("bxxxxxx111",9), comparison=ComparisonOperation.NOT_EQUAL_NO_XY, move=True)
    if sample_C is None: return None

    # First word of the column command
    timestamp_column_command_w0 = self.CK_T.get_edge_at_timestamp(sample_C.timestamp, polarity=EdgePolarity.RISING, move=True).timestamp
    column_command_w0 = self.C.get_at_timestamp(timestamp_column_command_w0, move=True).value

    # Second word of the column command
    timestamp_column_command_w1 = self.CK_T.get_edge(polarity=EdgePolarity.FALLING, move=True).timestamp
    column_command_w1 = self.C.get_at_timestamp(timestamp_column_command_w1, move=True).value

    # Decode the column command function using the truth table
    column_command_function = HBM2eColumnCommand_Error
    if   column_command_w0.equal_no_xy(VCDValue("bxxxxx0101",9)): column_command_function = HBM2eColumnCommand_Read
    elif column_command_w0.equal_no_xy(VCDValue("bxxxxx1101",9)): column_command_function = HBM2eColumnCommand_ReadAutoPrecharge
    elif column_command_w0.equal_no_xy(VCDValue("bxxxxx0001",9)): column_command_function = HBM2eColumnCommand_Write
    elif column_command_w0.equal_no_xy(VCDValue("bxxxxx1001",9)): column_command_function = HBM2eColumnCommand_WriteAutoPrecharge
    elif column_command_w0.equal_no_xy(VCDValue("bxxxxxx000",9)): column_command_function = HBM2eColumnCommand_ModeRegisterSet

    # Decode the operands of the function
    column_command = HBM2eColumnCommand_Error(timestamp = timestamp_column_command_w0)
    if column_command_function == HBM2eColumnCommand_Read:
      parity         =     column_command_w1[2]
      pseudo_channel =     column_command_w1[7]
      stack_id       = (   column_command_w0[8]
                        ** column_command_w1[0])
      bank_address   =     column_command_w0[4:7]
      column_address = (   column_command_w1[3:7]
                        ** column_command_w1[1]) << 1
      column_command = HBM2eColumnCommand_Read (
        timestamp      = timestamp_column_command_w0,
        parity         = parity,
        pseudo_channel = pseudo_channel,
        stack_id       = stack_id,
        bank_address   = bank_address,
        column_address = column_address,
      )
    elif column_command_function == HBM2eColumnCommand_ReadAutoPrecharge:
      parity         =     column_command_w1[2]
      pseudo_channel =     column_command_w1[7]
      stack_id       = (   column_command_w0[8]
                        ** column_command_w1[0])
      bank_address   =     column_command_w0[4:7]
      column_address = (   column_command_w1[3:7]
                        ** column_command_w1[1]) << 1
      column_command = HBM2eColumnCommand_ReadAutoPrecharge (
        timestamp      = timestamp_column_command_w0,
        parity         = parity,
        pseudo_channel = pseudo_channel,
        stack_id       = stack_id,
        bank_address   = bank_address,
        column_address = column_address,
      )
    if column_command_function == HBM2eColumnCommand_Write:
      parity         =     column_command_w1[2]
      pseudo_channel =     column_command_w1[7]
      stack_id       = (   column_command_w0[8]
                        ** column_command_w1[0])
      bank_address   =     column_command_w0[4:7]
      column_address = (   column_command_w1[3:7]
                        ** column_command_w1[1]) << 1
      column_command = HBM2eColumnCommand_Write (
        timestamp      = timestamp_column_command_w0,
        parity         = parity,
        pseudo_channel = pseudo_channel,
        stack_id       = stack_id,
        bank_address   = bank_address,
        column_address = column_address,
      )
    elif column_command_function == HBM2eColumnCommand_WriteAutoPrecharge:
      parity         =     column_command_w1[2]
      pseudo_channel =     column_command_w1[7]
      stack_id       = (   column_command_w0[8]
                        ** column_command_w1[0])
      bank_address   =     column_command_w0[4:7]
      column_address = (   column_command_w1[3:7]
                        ** column_command_w1[1]) << 1
      column_command = HBM2eColumnCommand_WriteAutoPrecharge (
        timestamp      = timestamp_column_command_w0,
        parity         = parity,
        pseudo_channel = pseudo_channel,
        stack_id       = stack_id,
        bank_address   = bank_address,
        column_address = column_address,
      )
    elif column_command_function == HBM2eColumnCommand_ModeRegisterSet:
      parity        =     column_command_w1[2]
      mode_register =     column_command_w0[4:7]
      operation     = (   column_command_w1[3:8]
                       ** column_command_w1[0:2])
      column_command = HBM2eColumnCommand_ModeRegisterSet (
        timestamp     = timestamp_column_command_w0,
        parity        = parity,
        mode_register = mode_register,
        operation     = operation,
      )

    # Fetch the data
    data_latency    = None
    strobe_signal_t = None
    if column_command_function in [HBM2eColumnCommand_Read, HBM2eColumnCommand_ReadAutoPrecharge]:
      data_latency    = read_latency
      strobe_signal_t = self.RDQS_T
      strobe_signal_c = self.RDQS_C
    elif column_command_function in [HBM2eColumnCommand_Write, HBM2eColumnCommand_WriteAutoPrecharge]:
      data_latency    = write_latency
      strobe_signal_t = self.WDQS_T
      strobe_signal_c = self.WDQS_C

    if data_latency is not None:

      # Pseudo-channels use different halves of the DQ and *DQS buses
      data_bus_slice       = None
      auxiliary_bus_slice  = None
      strobe_bus_reference = None
      if column_command.pseudo_channel.decimal() == 1:
        data_bus_slice       = slice(64,128)
        auxiliary_bus_slice  = slice(8,16)
        strobe_bus_reference = VCDValue("b11xx",4)
      else:
        data_bus_slice       = slice(0,64)
        auxiliary_bus_slice  = slice(0,8)
        strobe_bus_reference = VCDValue("bxx11",4)

      # Use the CK_c to move half a tCK before the data burst
      self.CK_C.get_edge_at_timestamp(timestamp_column_command_w0, move=True)
      for t_ck in range(data_latency-1):
        self.CK_C.get_edge(move=True)

      # Move to the first beat using the read strobe
      strobe_signal_t.get_at_timestamp(self.CK_C.current_sample.timestamp, move=True)
      strobe_signal_c.get_at_timestamp(self.CK_C.current_sample.timestamp, move=True)

      # Capture the beats of the data burst
      beat_timestamp = None
      even_beat      = True
      data_burst     = VCDValue.none()
      for beat in range(burst_length):

        # Capture on rising edge of the t or c data strobe
        if even_beat:
          beat_timestamp = strobe_signal_t.get_edge(value=strobe_bus_reference, move=True).timestamp
        else:
          beat_timestamp = strobe_signal_c.get_edge(value=strobe_bus_reference, move=True).timestamp
        even_beat = not even_beat

        # Read the half of the data bus corresponding to the pseudo-channel
        data_beat = self.DQ.get_at_timestamp(beat_timestamp, move=True).value[data_bus_slice]

        # Data bus inversion
        if enable_data_bus_inversion:
          data_bus_inversion_beat = self.DBI.get_at_timestamp(beat_timestamp, move=True).value[auxiliary_bus_slice]
          for byte_index in range(data_bus_inversion_beat.width):
            if data_bus_inversion_beat[byte_index]:
              data_byte_slice = slice(byte_index * 8, (byte_index+1) * 8)
              data_beat[data_byte_slice] = ~data_beat[data_byte_slice]

        # Switch the two halves of the data beat
        data_beat = data_beat[:len(data_beat)//2] ** data_beat[len(data_beat)//2:]

        # Append the data to the burst
        data_burst **= data_beat

      # Set the data of the command
      column_command.data = data_burst

    return column_command



  def column_commands(self) -> Generator[HBM2eColumnCommand, None, None]:
    """ Generator to iterate over all column commands. """
    while True:
      try:
        next_column_command = self.next_column_command()
        if next_column_command:
          yield next_column_command
        else: return
      except: return






column_address_width = 5 # Only CA1 to CA5 in HBM2e mode
row_address_width    = 15
bank_address_width   = 4
stack_id_width       = 1

columns_per_row            = 2**column_address_width
rows_per_bank              = 2**row_address_width
banks_per_stack            = 2**bank_address_width
banks_per_pseudo_channel   = 2**stack_id_width * banks_per_stack
pseudo_channel_per_channel = 2
banks_per_channel          = pseudo_channel_per_channel * banks_per_pseudo_channel

symbol_bank_inactive        = Color.FAINT  + '│' + Color.RESET
symbol_bank_activate        = Color.RED    + '█' + Color.RESET
symbol_bank_precharge       = Color.GREEN  + '█' + Color.RESET
symbol_bank_read            = Color.YELLOW + '█' + Color.RESET
symbol_bank_read_precharge  = Color.YELLOW + '█' + Color.RESET
symbol_bank_write           = Color.CYAN   + '█' + Color.RESET
symbol_bank_write_precharge = Color.CYAN   + '█' + Color.RESET
symbol_bank_refresh         = Color.BLUE   + '█' + Color.RESET
symbol_bank_idle            =                '┃'

class HBM2eBankAnnotator(Annotator):
  """ Display the status and activity of all banks. """

  def __init__(self):
    """ At initialization, all banks are considered inactive and the annotation string is empty. """
    self.banks_active      = [False] * banks_per_channel
    self.annotation_string = " "     * banks_per_channel

  def update(self, command:HBM2eCommand):
    """ Update the annotator status and string with a command. """

    # Use an annotation list instead of a string to store for each bank the character and optional ANSI format codes
    annotation_list = []

    # Line for activated and inactive banks
    for bank_index in range(banks_per_channel):
      annotation_list.append(symbol_bank_idle if self.banks_active[bank_index] else symbol_bank_inactive)

    # For commands addressing pseudo-channels
    pseudo_channel = None
    pseudo_channel_banks_slice = None
    def fetch_pseudo_channel():
      nonlocal pseudo_channel
      nonlocal pseudo_channel_banks_slice
      pseudo_channel = command.pseudo_channel.decimal()
      pseudo_channel_banks_slice = slice( pseudo_channel      * banks_per_pseudo_channel,
                                         (pseudo_channel + 1) * banks_per_pseudo_channel)

    # For commands addressing banks
    stack_id     = None
    bank_address = None
    bank_index   = None
    def fetch_bank_index():
      nonlocal stack_id
      nonlocal bank_address
      nonlocal bank_index
      stack_id     = command.stack_id.decimal()
      bank_address = command.bank_address.decimal()
      bank_index   = pseudo_channel * banks_per_pseudo_channel  +  stack_id * banks_per_stack  +  bank_address

    # Only consider row and column commands that affect the bank status or perform operations on banks.
    # For each command, fetch the corresponding addresses, update the annotation, and update the bank status.
    match command:

      case HBM2eRowCommand_Activate():
        fetch_pseudo_channel()
        fetch_bank_index()
        annotation_list[bank_index] = symbol_bank_activate
        self.banks_active[bank_index] = True

      case HBM2eRowCommand_Precharge():
        fetch_pseudo_channel()
        fetch_bank_index()
        annotation_list[bank_index] = symbol_bank_precharge
        self.banks_active[bank_index] = False

      case HBM2eRowCommand_PrechargeAll():
        fetch_pseudo_channel()
        annotation_list[pseudo_channel_banks_slice] = [symbol_bank_refresh] * symbol_bank_precharge
        self.banks_active = [False] * banks_per_channel

      case HBM2eRowCommand_SingleBankRefresh():
        fetch_pseudo_channel()
        fetch_bank_index()
        annotation_list[bank_index] = symbol_bank_refresh

      case HBM2eRowCommand_Refresh():
        fetch_pseudo_channel()
        annotation_list[pseudo_channel_banks_slice] = [symbol_bank_refresh] * banks_per_pseudo_channel

      case HBM2eColumnCommand_Read():
        fetch_pseudo_channel()
        fetch_bank_index()
        annotation_list[bank_index] = symbol_bank_read

      case HBM2eColumnCommand_ReadAutoPrecharge():
        fetch_pseudo_channel()
        fetch_bank_index()
        annotation_list[bank_index] = symbol_bank_read
        self.banks_active[bank_index] = False

      case HBM2eColumnCommand_Write():
        fetch_pseudo_channel()
        fetch_bank_index()
        annotation_list[bank_index] = symbol_bank_write

      case HBM2eColumnCommand_WriteAutoPrecharge():
        fetch_pseudo_channel()
        fetch_bank_index()
        annotation_list[bank_index] = symbol_bank_write
        self.banks_active[bank_index] = False

      case _:
        pass

    # Convert the annotation list to a single string
    self.annotation_string = "".join(annotation_list)

  def __repr__(self):
    """ Get the current annotation string. """
    return self.annotation_string






symbol_column_inactive        = Color.RED + Color.BLINK + '╳' + Color.RESET
symbol_column_activate        = Color.RED    + '━' + Color.RESET
symbol_column_precharge_all   = Color.GREEN  + '━' + Color.RESET
symbol_column_unused          = Color.FAINT  + '╌' + Color.RESET
symbol_column_do_read         = Color.YELLOW + '█' + Color.RESET
symbol_column_do_write        = Color.CYAN   + '█' + Color.RESET
symbol_column_is_read         = Color.WHITE  + '╍' + Color.RESET
symbol_column_is_written      = Color.WHITE  + '━' + Color.RESET
column_precharge_color        = Color.GREEN

class HBM2ePageStatus(Enum):
  """ Status for a column of a page. """
  INACTIVE  = 0
  UNUSED    = 1
  READ      = 2
  WRITTEN   = 3

class HBM2ePageAnnotator(Annotator):
  """ Display the status and activity of the page accessed. """

  def __init__(self):
    """ At initialization, all columns are considered unused and the annotation string is empty. """
    self.pages_status = [[HBM2ePageStatus.UNUSED] * columns_per_row for bank in range(banks_per_channel)]
    self.annotation_string = " " * columns_per_row

  def update(self, command:HBM2eCommand):
    """ Update the annotator status and string with a command. """

    # Use an annotation list instead of a string to store for each bank the character and optional ANSI format codes
    annotation_list = [" "] * columns_per_row

    # For commands addressing pseudo-channels
    pseudo_channel = None
    def fetch_pseudo_channel():
      nonlocal pseudo_channel
      pseudo_channel = command.pseudo_channel.decimal()

    # For commands addressing banks
    stack_id     = None
    bank_address = None
    bank_index   = None
    def fetch_bank_index():
      nonlocal stack_id
      nonlocal bank_address
      nonlocal bank_index
      stack_id     = command.stack_id.decimal()
      bank_address = command.bank_address.decimal()
      bank_index   = pseudo_channel * banks_per_pseudo_channel  +  stack_id * banks_per_stack  +  bank_address

    # For commands addressing columns
    column_address = None
    column_index   = None
    def fetch_column_index():
      nonlocal column_address
      nonlocal column_index
      column_address = command.column_address.decimal()
      column_index   = column_address // 2

    # Load the status of the page of a bank and update the annotation
    def load_page_status():
      nonlocal annotation_list
      annotation_list = []
      page_status = self.pages_status[bank_index]
      for column_index in range(columns_per_row):
        match page_status[column_index]:
          case HBM2ePageStatus.INACTIVE:
            annotation_list.append(symbol_column_inactive)
          case HBM2ePageStatus.UNUSED:
            annotation_list.append(symbol_column_unused)
          case HBM2ePageStatus.READ:
            annotation_list.append(symbol_column_is_read)
          case HBM2ePageStatus.WRITTEN:
            annotation_list.append(symbol_column_is_written)

    # Update the page status after an activation (all columns are unused)
    def activate_page_status():
      nonlocal bank_index
      self.pages_status[bank_index] = [HBM2ePageStatus.UNUSED] * columns_per_row

    # Clear the page status after a precharge (all columns are inactive)
    def clear_page_status():
      nonlocal bank_index
      self.pages_status[bank_index] = [HBM2ePageStatus.INACTIVE] * columns_per_row

    # Clear all page status after a precharge all banks (all columns are inactive)
    def clear_all_page_status():
      self.pages_status = [[HBM2ePageStatus.UNUSED] * columns_per_row for bank in range(banks_per_channel)]

    # For a precharge, the character for all columns gets a special ANSI formatting
    def apply_precharge_format():
      # Iterate over the symbols of all columns
      for column_index in range(columns_per_row):
        # Remove the previous color
        annotation_list[column_index] = remove_colors(annotation_list[column_index])
        # Add the color of precharge
        annotation_list[column_index] = column_precharge_color + annotation_list[column_index] + Color.RESET

    # Only consider row and column commands that affect the bank status or perform operations on banks.
    # For each command, fetch the corresponding addresses, update the annotation, and update the page status.
    match command:

      case HBM2eRowCommand_Activate():
        fetch_pseudo_channel()
        fetch_bank_index()
        annotation_list = [symbol_column_activate] * columns_per_row
        activate_page_status()

      case HBM2eRowCommand_Precharge():
        fetch_pseudo_channel()
        fetch_bank_index()
        load_page_status()
        apply_precharge_format()
        clear_page_status()

      case HBM2eRowCommand_PrechargeAll():
        fetch_pseudo_channel()
        annotation_list = [symbol_column_precharge_all] * columns_per_row
        clear_all_page_status()

      case HBM2eColumnCommand_Read():
        fetch_pseudo_channel()
        fetch_bank_index()
        load_page_status()
        fetch_column_index()
        annotation_list[column_index] = symbol_column_do_read
        # If the column was in the state written, don't overwrite with read
        if self.pages_status[bank_index][column_index] != HBM2ePageStatus.WRITTEN:
          self.pages_status[bank_index][column_index] = HBM2ePageStatus.READ

      case HBM2eColumnCommand_ReadAutoPrecharge():
        fetch_pseudo_channel()
        fetch_bank_index()
        load_page_status()
        apply_precharge_format()
        fetch_column_index()
        annotation_list[column_index] = symbol_column_do_read
        clear_page_status()

      case HBM2eColumnCommand_Write():
        fetch_pseudo_channel()
        fetch_bank_index()
        load_page_status()
        fetch_column_index()
        annotation_list[column_index] = symbol_column_do_write
        self.pages_status[bank_index][column_index] = HBM2ePageStatus.WRITTEN

      case HBM2eColumnCommand_WriteAutoPrecharge():
        fetch_pseudo_channel()
        fetch_bank_index()
        load_page_status()
        apply_precharge_format()
        fetch_column_index()
        annotation_list[column_index] = symbol_column_do_write
        clear_page_status()

      case _:
        pass

    # Convert the annotation list to a single string
    self.annotation_string = "".join(annotation_list)

  def __repr__(self):
    """ Get the current annotation string. """
    return self.annotation_string






word_length           = 32
number_words          = data_width // 32
data_annotation_width = number_words * (word_length // 4 + 1) - 1

class HBM2eDataAnnotator(Annotator):
  """ Display the content of the data bus for reads and writes. """

  def __init__(self):
    """ At initialization, the annotation string is empty. """
    self.annotation_string = " " * data_annotation_width

  def update(self, command:HBM2eCommand):
    """ Update the annotator string with a command. """

    # Only reads and writes have data
    if type(command) in [HBM2eColumnCommand_Read,
                         HBM2eColumnCommand_ReadAutoPrecharge,
                         HBM2eColumnCommand_Write,
                         HBM2eColumnCommand_WriteAutoPrecharge]:

      # Use an annotation list instead of a string to store for each bank the character and optional ANSI format codes
      annotation_list = []

      # Separate the burst data into words for easier reading
      for word_index in range(number_words):
        word_value = command.data[ word_index    * word_length :
                                  (word_index+1) * word_length ]
        word_string = word_value.hexadecimal()
        # Mark zeros with a faint color for easier reading
        word_string = word_string.replace('0', Color.FAINT + '0' + Color.RESET)
        annotation_list.append(word_string)

      # Convert the annotation list to a single string
      self.annotation_string = " ".join(annotation_list)

    else:
      # Empty string for commands without data
      self.annotation_string = " " * data_annotation_width

  def __repr__(self):
    """ Get the current annotation string. """
    return self.annotation_string
