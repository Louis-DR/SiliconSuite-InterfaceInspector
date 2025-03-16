from dataclasses import dataclass
from typing import Generator
from .vcd import VCDFile, VCDValue, ComparisonOperation, EdgePolarity
from .utils import change_case, command_str, Color






command_width = 6
context_width = 0
value_width   = 2
line_width    = 62

class DDR5Command:
  """ DDR5 command base type. """
  def __str__(self):
    return self.__repr__()

class DDR5Command_Error(DDR5Command):
  """ DDR5 incorrect command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
  def __repr__(self):
    parameters = {}
    return command_str(
      timestamp  = self.timestamp,
      command    = "ERROR",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_BLACK + Color.RED + Color.BLINK,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_Activate(DDR5Command):
  """ DDR5 activate command. """
  def __init__(self,
               timestamp          : int,
               chip_select        : VCDValue,
               chip_id            : VCDValue,
               bank_group_address : VCDValue,
               bank_address       : VCDValue,
               row_address        : VCDValue):
    self.timestamp          = timestamp
    self.chip_select        = chip_select
    self.chip_id            = chip_id
    self.bank_group_address = bank_group_address
    self.bank_address       = bank_address
    self.row_address        = row_address
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id            .decimal()
    parameters["BG"]  = self.bank_group_address .decimal()
    parameters["BA"]  = self.bank_address       .decimal()
    parameters["R"]   = self.row_address        .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "ACT",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_RED,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_WritePattern(DDR5Command):
  """ DDR5 write pattern command. """
  def __init__(self,
               timestamp          : int,
               chip_select        : VCDValue,
               chip_id            : VCDValue,
               bank_group_address : VCDValue,
               bank_address       : VCDValue,
               column_address     : VCDValue):
    self.timestamp          = timestamp
    self.chip_select        = chip_select
    self.chip_id            = chip_id
    self.bank_group_address = bank_group_address
    self.bank_address       = bank_address
    self.column_address     = column_address
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id            .decimal()
    parameters["BG"]  = self.bank_group_address .decimal()
    parameters["BA"]  = self.bank_address       .decimal()
    parameters["C"]   = self.column_address     .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "WRP",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_CYAN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_WritePatternAutoPrecharge(DDR5Command):
  """ DDR5 write pattern with auto-precharge command. """
  def __init__(self,
               timestamp          : int,
               chip_select        : VCDValue,
               chip_id            : VCDValue,
               bank_group_address : VCDValue,
               bank_address       : VCDValue,
               column_address     : VCDValue):
    self.timestamp          = timestamp
    self.chip_select        = chip_select
    self.chip_id            = chip_id
    self.bank_group_address = bank_group_address
    self.bank_address       = bank_address
    self.column_address     = column_address
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id            .decimal()
    parameters["BG"]  = self.bank_group_address .decimal()
    parameters["BA"]  = self.bank_address       .decimal()
    parameters["C"]   = self.column_address     .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "WRPA",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_CYAN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_ModeRegisterWrite(DDR5Command):
  """ DDR5 mode register write command. """
  def __init__(self,
               timestamp     : int,
               chip_select   : VCDValue,
               mode_register : VCDValue,
               operation     : VCDValue,
               control_word  : VCDValue):
    self.timestamp     = timestamp
    self.chip_select   = chip_select
    self.mode_register = mode_register
    self.operation     = operation
    self.control_word  = control_word
  def __repr__(self):
    parameters = {}
    parameters["MRA"] = self.mode_register .decimal()
    parameters["OP"]  = self.operation     .decimal()
    parameters["CW"]  = self.control_word  .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "MRW",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_MAGENTA,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_ModeRegisterRead(DDR5Command):
  """ DDR5 mode register read command. """
  def __init__(self,
               timestamp     : int,
               chip_select   : VCDValue,
               mode_register : VCDValue,
               control_word  : VCDValue):
    self.timestamp     = timestamp
    self.chip_select   = chip_select
    self.mode_register = mode_register
    self.control_word  = control_word
  def __repr__(self):
    parameters = {}
    parameters["MRA"] = self.mode_register .decimal()
    parameters["CW"]  = self.control_word  .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "MRR",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_MAGENTA,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_Write(DDR5Command):
  """ DDR5 write command. """
  def __init__(self,
               timestamp          : int,
               chip_select        : VCDValue,
               chip_id            : VCDValue,
               bank_group_address : VCDValue,
               bank_address       : VCDValue,
               column_address     : VCDValue,
               burst_length       : VCDValue,
               partial_write      : VCDValue):
    self.timestamp          = timestamp
    self.chip_select        = chip_select
    self.chip_id            = chip_id
    self.bank_group_address = bank_group_address
    self.bank_address       = bank_address
    self.column_address     = column_address
    self.burst_length       = burst_length
    self.partial_write      = partial_write
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id            .decimal()
    parameters["BG"]  = self.bank_group_address .decimal()
    parameters["BA"]  = self.bank_address       .decimal()
    parameters["C"]   = self.column_address     .decimal()
    parameters["BL"]  = self.burst_length       .decimal()
    parameters["WRP"] = self.partial_write      .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "WR",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_CYAN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_WriteAutoPrecharge(DDR5Command):
  """ DDR5 write with auto-precharge command. """
  def __init__(self,
               timestamp          : int,
               chip_select        : VCDValue,
               chip_id            : VCDValue,
               bank_group_address : VCDValue,
               bank_address       : VCDValue,
               column_address     : VCDValue,
               burst_length       : VCDValue,
               partial_write      : VCDValue):
    self.timestamp          = timestamp
    self.chip_select        = chip_select
    self.chip_id            = chip_id
    self.bank_group_address = bank_group_address
    self.bank_address       = bank_address
    self.column_address     = column_address
    self.burst_length       = burst_length
    self.partial_write      = partial_write
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id            .decimal()
    parameters["BG"]  = self.bank_group_address .decimal()
    parameters["BA"]  = self.bank_address       .decimal()
    parameters["C"]   = self.column_address     .decimal()
    parameters["BL"]  = self.burst_length       .decimal()
    parameters["WRP"] = self.partial_write      .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "WRA",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_CYAN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_Read(DDR5Command):
  """ DDR5 read command. """
  def __init__(self,
               timestamp          : int,
               chip_select        : VCDValue,
               chip_id            : VCDValue,
               bank_group_address : VCDValue,
               bank_address       : VCDValue,
               column_address     : VCDValue,
               burst_length       : VCDValue):
    self.timestamp          = timestamp
    self.chip_select        = chip_select
    self.chip_id            = chip_id
    self.bank_group_address = bank_group_address
    self.bank_address       = bank_address
    self.column_address     = column_address
    self.burst_length       = burst_length
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id            .decimal()
    parameters["BG"]  = self.bank_group_address .decimal()
    parameters["BA"]  = self.bank_address       .decimal()
    parameters["C"]   = self.column_address     .decimal()
    parameters["BL"]  = self.burst_length       .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "RD",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_YELLOW,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_ReadAutoPrecharge(DDR5Command):
  """ DDR5 read with auto-precharge command. """
  def __init__(self,
               timestamp          : int,
               chip_select        : VCDValue,
               chip_id            : VCDValue,
               bank_group_address : VCDValue,
               bank_address       : VCDValue,
               column_address     : VCDValue,
               burst_length       : VCDValue):
    self.timestamp          = timestamp
    self.chip_select        = chip_select
    self.chip_id            = chip_id
    self.bank_group_address = bank_group_address
    self.bank_address       = bank_address
    self.column_address     = column_address
    self.burst_length       = burst_length
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id            .decimal()
    parameters["BG"]  = self.bank_group_address .decimal()
    parameters["BA"]  = self.bank_address       .decimal()
    parameters["C"]   = self.column_address     .decimal()
    parameters["BL"]  = self.burst_length       .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "RDA",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_YELLOW,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_VrefCA(DDR5Command):
  """ DDR5 VrefCA command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue,
               operation   : VCDValue,):
    self.timestamp   = timestamp
    self.chip_select = chip_select
    self.operation   = operation
  def __repr__(self):
    parameters = {}
    parameters["OP"] = self.operation.decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "VrefCA",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_MAGENTA,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_VrefCS(DDR5Command):
  """ DDR5 VrefCS command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue,
               operation   : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
    self.operation   = operation
  def __repr__(self):
    parameters = {}
    parameters["OP"] = self.operation.decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "VrefCS",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_MAGENTA,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_RefreshAll(DDR5Command):
  """ DDR5 refresh all command. """
  def __init__(self,
               timestamp             : int,
               chip_select           : VCDValue,
               chip_id               : VCDValue,
               refresh_interval_rate : VCDValue):
    self.timestamp             = timestamp
    self.chip_select           = chip_select
    self.chip_id               = chip_id
    self.refresh_interval_rate = refresh_interval_rate
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id               .decimal()
    parameters["RIR"] = self.refresh_interval_rate .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "REFab",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_BLUE,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_RefreshManagementAll(DDR5Command):
  """ DDR5 refresh management all command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue,
               chip_id     : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
    self.chip_id     = chip_id
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id.decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "RFMab",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_BLUE,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_RefreshSameBank(DDR5Command):
  """ DDR5 refresh same bank command. """
  def __init__(self,
               timestamp             : int,
               chip_select           : VCDValue,
               chip_id               : VCDValue,
               bank_address          : VCDValue,
               refresh_interval_rate : VCDValue):
    self.timestamp             = timestamp
    self.chip_select           = chip_select
    self.chip_id               = chip_id
    self.bank_address          = bank_address
    self.refresh_interval_rate = refresh_interval_rate
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id               .decimal()
    parameters["BA"]  = self.bank_address          .decimal()
    parameters["RIR"] = self.refresh_interval_rate .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "REFsb",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_BLUE,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_RefreshManagementSameBank(DDR5Command):
  """ DDR5 refresh management same bank command. """
  def __init__(self,
               timestamp    : int,
               chip_select  : VCDValue,
               chip_id      : VCDValue,
               bank_address : VCDValue):
    self.timestamp    = timestamp
    self.chip_select  = chip_select
    self.chip_id      = chip_id
    self.bank_address = bank_address
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id               .decimal()
    parameters["BA"]  = self.bank_address          .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "RFMsb",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_BLUE,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_PrechargeAll(DDR5Command):
  """ DDR5 precharge all command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue,
               chip_id     : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
    self.chip_id     = chip_id
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id.decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "PREab",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_GREEN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_PrechargeSameBank(DDR5Command):
  """ DDR5 precharge same bank command. """
  def __init__(self,
               timestamp    : int,
               chip_select  : VCDValue,
               chip_id      : VCDValue,
               bank_address : VCDValue):
    self.timestamp    = timestamp
    self.chip_select  = chip_select
    self.chip_id      = chip_id
    self.bank_address = bank_address
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id      .decimal()
    parameters["BA"]  = self.bank_address .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "PREab",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_GREEN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_Precharge(DDR5Command):
  """ DDR5 precharge command. """
  def __init__(self,
               timestamp          : int,
               chip_select        : VCDValue,
               chip_id            : VCDValue,
               bank_group_address : VCDValue,
               bank_address       : VCDValue):
    self.timestamp          = timestamp
    self.chip_select        = chip_select
    self.chip_id            = chip_id
    self.bank_group_address = bank_group_address
    self.bank_address       = bank_address
  def __repr__(self):
    parameters = {}
    parameters["CID"] = self.chip_id            .decimal()
    parameters["BG"]  = self.bank_group_address .decimal()
    parameters["BA"]  = self.bank_address       .decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "PREpb",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_GREEN,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_SelfRefreshEntry(DDR5Command):
  """ DDR5 self refresh entry command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
  def __repr__(self):
    parameters = {}
    return command_str(
      timestamp  = self.timestamp,
      command    = "SRE",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_WHITE + Color.BLACK,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_SelfRefreshEntryWithFrequencyChange(DDR5Command):
  """ DDR5 self refresh entry with frequency change command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
  def __repr__(self):
    parameters = {}
    return command_str(
      timestamp  = self.timestamp,
      command    = "SREF",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_WHITE + Color.BLACK,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_PowerDownEntry(DDR5Command):
  """ DDR5 power down entry command. """
  def __init__(self,
               timestamp          : int,
               chip_select        : VCDValue,
               on_die_termination : VCDValue):
    self.timestamp          = timestamp
    self.chip_select        = chip_select
    self.on_die_termination = on_die_termination
  def __repr__(self):
    parameters = {}
    parameters["ODT"] = self.on_die_termination.decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "PDE",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_WHITE + Color.BLACK,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )

class DDR5Command_MultiPurposeCommand(DDR5Command):
  """ DDR5 multi-purpose command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue,
               operation   : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
    self.operation   = operation
  def __repr__(self):
    parameters = {}
    parameters["OP"] = self.operation.decimal()
    return command_str(
      timestamp  = self.timestamp,
      command    = "MPC",
      parameters = parameters,
      context    = f"CS{self.chip_select.decimal()}",
      color      = Color.BG_MAGENTA,
      command_width = command_width,
      context_width = context_width,
      value_width   = value_width,
      line_width    = line_width
    )






@dataclass
class DDR5InterfacePaths:
  """ A set of DDR5 signal paths. """
  CK_T  : str = "CK_T"
  CK_C  : str = "CK_C"
  CS_N  : str = "CS_N"
  CA    : str = "CA"
  DQS_T : str = "DQS_T"
  DQS_C : str = "DQS_C"
  DQ    : str = "DQ"
  CB    : str = "CB"

class DDR5Interface:
  """ A DDR5 interface with its VCD signals. """
  def __init__(self,
               vcd_file  : VCDFile,
               signals   : DDR5InterfacePaths = None,
               path      : str                = "",
               prefix    : str                = "",
               suffix    : str                = "",
               uppercase : bool               = True):
    """ Get all the signals of the DDR5 bus. """
    if signals is None:
      self.paths = DDR5InterfacePaths()
      self.paths.CK_T  = f"{path}.{prefix}{change_case('CK_T',  uppercase)}{suffix}"
      self.paths.CK_C  = f"{path}.{prefix}{change_case('CK_C',  uppercase)}{suffix}"
      self.paths.CS_N  = f"{path}.{prefix}{change_case('CS_N',  uppercase)}{suffix}"
      self.paths.CA    = f"{path}.{prefix}{change_case('CA',    uppercase)}{suffix}"
      self.paths.DQS_T = f"{path}.{prefix}{change_case('DQS_T', uppercase)}{suffix}"
      self.paths.DQS_C = f"{path}.{prefix}{change_case('DQS_C', uppercase)}{suffix}"
      self.paths.DQ    = f"{path}.{prefix}{change_case('DQ',    uppercase)}{suffix}"
      self.paths.CB    = f"{path}.{prefix}{change_case('CB',    uppercase)}{suffix}"
    else: self.paths = signals
    self.CK_T  = vcd_file.get_signal( self.paths.CK_T  .split('.') )
    self.CK_C  = vcd_file.get_signal( self.paths.CK_C  .split('.') )
    self.CS_N  = vcd_file.get_signal( self.paths.CS_N  .split('.') )
    self.CA    = vcd_file.get_signal( self.paths.CA    .split('.') )
    self.DQS_T = vcd_file.get_signal( self.paths.DQS_T .split('.') )
    self.DQS_C = vcd_file.get_signal( self.paths.DQS_C .split('.') )
    self.DQ    = vcd_file.get_signal( self.paths.DQ    .split('.') )
    self.CB    = vcd_file.get_signal( self.paths.CB    .split('.') )



  def next_command(self) -> DDR5Command:
    """ Get the next DDR5 command. """

    # Get the next command
    chip_select_width = self.CS_N.width
    chip_select_idle = VCDValue("b"+chip_select_width*"1",chip_select_width)
    sample_CSN = self.CS_N.get_edge(value=chip_select_idle, comparison=ComparisonOperation.NOT_EQUAL_NO_XY, move=True)
    if sample_CSN is None: return None

    # Decode the chip select
    chip_select = 0
    for chip_select_index in range(chip_select_width):
      chip_select_test = VCDValue("b"+(chip_select_width-chip_select_index-1)*"1"+"0"+chip_select_index*"1", chip_select_width)
      if sample_CSN.value.equal_no_xy(chip_select_test):
        chip_select = VCDValue(f"r{chip_select_index}",0)
        break

    # Four words (UIs) of the command
    command_words = []
    command_words_timestamps = [self.CK_T.get_edge_at_timestamp(sample_CSN.timestamp, polarity=EdgePolarity.RISING).timestamp]
    for word_index in range(4):
      command_words.append(self.CA.get_at_timestamp(command_words_timestamps[-1], move=True).value)
      command_words_timestamps.append(self.CK_T.get_edge(polarity=EdgePolarity.RISING, move=True).timestamp)

    # Decode the command function using the truth table
    # Note: we are only focusing on the main decoding bits of the command truth table (not the H/L not highlighted in the specification)
    command_function = DDR5Command_Error
    if   command_words[0].equal_no_xy(VCDValue("bxxxxx00",7)):                                                          command_function = DDR5Command_Activate
    elif command_words[0].equal_no_xy(VCDValue("bxx01001",7)) and command_words[3].equal_no_xy(VCDValue("bxxx1xxx",7)): command_function = DDR5Command_WritePattern
    elif command_words[0].equal_no_xy(VCDValue("bxx01001",7)) and command_words[3].equal_no_xy(VCDValue("bxxx0xxx",7)): command_function = DDR5Command_WritePatternAutoPrecharge
    elif command_words[0].equal_no_xy(VCDValue("bxx00101",7))                                                         : command_function = DDR5Command_ModeRegisterWrite
    elif command_words[0].equal_no_xy(VCDValue("bxx10101",7))                                                         : command_function = DDR5Command_ModeRegisterRead
    elif command_words[0].equal_no_xy(VCDValue("bxx01101",7)) and command_words[3].equal_no_xy(VCDValue("bxxx1xxx",7)): command_function = DDR5Command_Write
    elif command_words[0].equal_no_xy(VCDValue("bxx01101",7)) and command_words[3].equal_no_xy(VCDValue("bxxx0xxx",7)): command_function = DDR5Command_WriteAutoPrecharge
    elif command_words[0].equal_no_xy(VCDValue("bxx11101",7)) and command_words[3].equal_no_xy(VCDValue("bxxx1xxx",7)): command_function = DDR5Command_Read
    elif command_words[0].equal_no_xy(VCDValue("bxx11101",7)) and command_words[3].equal_no_xy(VCDValue("bxxx0xxx",7)): command_function = DDR5Command_ReadAutoPrecharge
    elif command_words[0].equal_no_xy(VCDValue("bxx00011",7)) and command_words[1].equal_no_xy(VCDValue("bx0xxxxx",7)): command_function = DDR5Command_VrefCA
    elif command_words[0].equal_no_xy(VCDValue("bxx00011",7)) and command_words[1].equal_no_xy(VCDValue("bx1xxxxx",7)): command_function = DDR5Command_VrefCS
    elif command_words[0].equal_no_xy(VCDValue("bxx10011",7)) and command_words[1].equal_no_xy(VCDValue("bxxx01xx",7)): command_function = DDR5Command_RefreshAll
    elif command_words[0].equal_no_xy(VCDValue("bxx10011",7)) and command_words[1].equal_no_xy(VCDValue("bxxx00xx",7)): command_function = DDR5Command_RefreshManagementAll
    elif command_words[0].equal_no_xy(VCDValue("bxx10011",7)) and command_words[1].equal_no_xy(VCDValue("bxxx11xx",7)): command_function = DDR5Command_RefreshSameBank
    elif command_words[0].equal_no_xy(VCDValue("bxx10011",7)) and command_words[1].equal_no_xy(VCDValue("bxxx10xx",7)): command_function = DDR5Command_RefreshManagementSameBank
    elif command_words[0].equal_no_xy(VCDValue("bxx01011",7)) and command_words[1].equal_no_xy(VCDValue("bxxx0xxx",7)): command_function = DDR5Command_PrechargeAll
    elif command_words[0].equal_no_xy(VCDValue("bxx01011",7)) and command_words[1].equal_no_xy(VCDValue("bxxx1xxx",7)): command_function = DDR5Command_PrechargeSameBank
    elif command_words[0].equal_no_xy(VCDValue("bxx11011",7))                                                         : command_function = DDR5Command_Precharge
    elif command_words[0].equal_no_xy(VCDValue("bxx10111",7)) and command_words[1].equal_no_xy(VCDValue("bxxx01xx",7)): command_function = DDR5Command_SelfRefreshEntry
    elif command_words[0].equal_no_xy(VCDValue("bxx10111",7)) and command_words[1].equal_no_xy(VCDValue("bxxx00xx",7)): command_function = DDR5Command_SelfRefreshEntryWithFrequencyChange
    elif command_words[0].equal_no_xy(VCDValue("bxx10111",7)) and command_words[1].equal_no_xy(VCDValue("bxxx1xxx",7)): command_function = DDR5Command_PowerDownEntry
    elif command_words[0].equal_no_xy(VCDValue("bxx01111",7))                                                         : command_function = DDR5Command_MultiPurposeCommand

    # Decode the operands of the function
    command = DDR5Command_Error(
      timestamp   = command_words_timestamps[0],
      chip_select = chip_select
    )

    if command_function == DDR5Command_Activate:
      chip_id            =     command_words[1][4:6]
      bank_group_address =     command_words[1][1:3]
      bank_address       = (   command_words[1][0]
                            ** command_words[0][6] )
      row_address        = (   command_words[3][0:6]
                            ** command_words[2][0:6]
                            ** command_words[0][2:5] )
      command = DDR5Command_Activate (
        timestamp          = command_words_timestamps[2],
        chip_select        = chip_select,
        chip_id            = chip_id,
        bank_group_address = bank_group_address,
        bank_address       = bank_address,
        row_address        = row_address,
      )

    elif command_function == DDR5Command_WritePattern:
      chip_id            =     command_words[1][4:6]
      bank_group_address =     command_words[1][1:3]
      bank_address       = (   command_words[1][0]
                            ** command_words[0][6] )
      column_address     = (   command_words[2][1:6]
                            ** command_words[3][0:1] ) << 3
      command = DDR5Command_WritePattern (
        timestamp          = command_words_timestamps[2],
        chip_select        = chip_select,
        chip_id            = chip_id,
        bank_group_address = bank_group_address,
        bank_address       = bank_address,
        column_address     = column_address,
      )

    elif command_function == DDR5Command_WritePatternAutoPrecharge:
      chip_id            =     command_words[1][4:6]
      bank_group_address =     command_words[1][1:3]
      bank_address       = (   command_words[1][0]
                            ** command_words[0][6] )
      column_address     = (   command_words[2][1:6]
                            ** command_words[3][0:1] ) << 3
      command = DDR5Command_WritePatternAutoPrecharge (
        timestamp          = command_words_timestamps[2],
        chip_select        = chip_select,
        chip_id            = chip_id,
        bank_group_address = bank_group_address,
        bank_address       = bank_address,
        column_address     = column_address,
      )

    elif command_function == DDR5Command_ModeRegisterWrite:
      mode_register = (   command_words[0][5:6]
                       ** command_words[1][0:5] )
      operation     = (   command_words[2][0:6]
                       ** command_words[3][0] )
      control_word  =     command_words[3][3]
      command = DDR5Command_ModeRegisterWrite (
        timestamp     = command_words_timestamps[2],
        chip_select   = chip_select,
        mode_register = mode_register,
        operation     = operation,
        control_word  = control_word,
      )

    elif command_function == DDR5Command_ModeRegisterRead:
      mode_register = (   command_words[0][5:6]
                       ** command_words[1][0:5] )
      control_word  =     command_words[3][3]
      command = DDR5Command_ModeRegisterRead (
        timestamp     = command_words_timestamps[2],
        chip_select   = chip_select,
        mode_register = mode_register,
        control_word  = control_word,
      )

    elif command_function == DDR5Command_Write:
      chip_id            =     command_words[1][4:6]
      bank_group_address =     command_words[1][1:3]
      bank_address       = (   command_words[1][0]
                            ** command_words[0][6] )
      column_address     = (   command_words[2][1:6]
                            ** command_words[3][0:1] ) << 3
      burst_length       =     command_words[0][5]
      partial_write      =     command_words[3][4]
      command = DDR5Command_Write (
        timestamp          = command_words_timestamps[2],
        chip_select        = chip_select,
        chip_id            = chip_id,
        bank_group_address = bank_group_address,
        bank_address       = bank_address,
        column_address     = column_address,
        burst_length       = burst_length,
        partial_write      = partial_write,
      )

    elif command_function == DDR5Command_WriteAutoPrecharge:
      chip_id            =     command_words[1][4:6]
      bank_group_address =     command_words[1][1:3]
      bank_address       = (   command_words[1][0]
                            ** command_words[0][6] )
      column_address     = (   command_words[2][1:6]
                            ** command_words[3][0:1] ) << 3
      burst_length       =     command_words[0][5]
      partial_write      =     command_words[3][4]
      command = DDR5Command_WriteAutoPrecharge (
        timestamp          = command_words_timestamps[2],
        chip_select        = chip_select,
        chip_id            = chip_id,
        bank_group_address = bank_group_address,
        bank_address       = bank_address,
        column_address     = column_address,
        burst_length       = burst_length,
        partial_write      = partial_write,
      )

    elif command_function == DDR5Command_Read:
      chip_id            =     command_words[1][4:6]
      bank_group_address =     command_words[1][1:3]
      bank_address       = (   command_words[1][0]
                            ** command_words[0][6] )
      column_address     = (   command_words[2][0:6]
                            ** command_words[3][0:1] ) << 2
      burst_length       =     command_words[0][5]
      command = DDR5Command_Read (
        timestamp          = command_words_timestamps[2],
        chip_select        = chip_select,
        chip_id            = chip_id,
        bank_group_address = bank_group_address,
        bank_address       = bank_address,
        column_address     = column_address,
        burst_length       = burst_length,
      )

    elif command_function == DDR5Command_ReadAutoPrecharge:
      chip_id            =     command_words[1][4:6]
      bank_group_address =     command_words[1][1:3]
      bank_address       = (   command_words[1][0]
                            ** command_words[0][6] )
      column_address     = (   command_words[2][0:6]
                            ** command_words[3][0:1] ) << 2
      burst_length       =     command_words[0][5]
      command = DDR5Command_ReadAutoPrecharge (
        timestamp          = command_words_timestamps[2],
        chip_select        = chip_select,
        chip_id            = chip_id,
        bank_group_address = bank_group_address,
        bank_address       = bank_address,
        column_address     = column_address,
        burst_length       = burst_length,
      )

    elif command_function == DDR5Command_VrefCA:
      operation = (   command_words[1][0:4]
                   ** command_words[0][5:6] )
      command = DDR5Command_VrefCA (
        timestamp   = command_words_timestamps[0],
        chip_select = chip_select,
        operation   = operation,
      )

    elif command_function == DDR5Command_VrefCS:
      operation = (   command_words[1][0:4]
                   ** command_words[0][5:6] )
      command = DDR5Command_VrefCS (
        timestamp   = command_words_timestamps[0],
        chip_select = chip_select,
        operation   = operation,
      )

    elif command_function == DDR5Command_RefreshAll:
      chip_id               = command_words[1][4:6]
      refresh_interval_rate = command_words[1][1]
      command = DDR5Command_RefreshAll (
        timestamp             = command_words_timestamps[0],
        chip_select           = chip_select,
        chip_id               = chip_id,
        refresh_interval_rate = refresh_interval_rate,
      )

    elif command_function == DDR5Command_RefreshManagementAll:
      chip_id = command_words[1][4:6]
      command = DDR5Command_RefreshManagementAll (
        timestamp   = command_words_timestamps[0],
        chip_select = chip_select,
        chip_id     = chip_id,
      )

    elif command_function == DDR5Command_RefreshSameBank:
      chip_id               = command_words[1][4:6]
      bank_address          = (   command_words[1][0]
                               ** command_words[0][6] )
      refresh_interval_rate = command_words[1][1]
      command = DDR5Command_RefreshSameBank (
        timestamp             = command_words_timestamps[0],
        chip_select           = chip_select,
        chip_id               = chip_id,
        bank_address          = bank_address,
        refresh_interval_rate = refresh_interval_rate,
      )

    elif command_function == DDR5Command_RefreshManagementSameBank:
      chip_id      = command_words[1][4:6]
      bank_address = (   command_words[1][0]
                      ** command_words[0][6] )
      command = DDR5Command_RefreshManagementSameBank (
        timestamp    = command_words_timestamps[0],
        chip_select  = chip_select,
        chip_id      = chip_id,
        bank_address = bank_address,
      )

    elif command_function == DDR5Command_PrechargeAll:
      chip_id = command_words[1][4:6]
      command = DDR5Command_PrechargeAll (
        timestamp   = command_words_timestamps[0],
        chip_select = chip_select,
        chip_id     = chip_id,
      )

    elif command_function == DDR5Command_PrechargeSameBank:
      chip_id = command_words[1][4:6]
      command = DDR5Command_PrechargeSameBank (
        timestamp    = command_words_timestamps[0],
        chip_select  = chip_select,
        chip_id      = chip_id,
        bank_address = bank_address,
      )

    elif command_function == DDR5Command_Precharge:
      chip_id            =     command_words[1][4:6]
      bank_group_address =     command_words[1][1:3]
      bank_address       = (   command_words[1][0]
                            ** command_words[0][6] )
      command = DDR5Command_Precharge (
        timestamp          = command_words_timestamps[0],
        chip_select        = chip_select,
        chip_id            = chip_id,
        bank_group_address = bank_group_address,
        bank_address       = bank_address,
      )

    elif command_function == DDR5Command_SelfRefreshEntry:
      command = DDR5Command_SelfRefreshEntry (
        timestamp   = command_words_timestamps[0],
        chip_select = chip_select,
      )

    elif command_function == DDR5Command_SelfRefreshEntryWithFrequencyChange:
      command = DDR5Command_SelfRefreshEntryWithFrequencyChange (
        timestamp   = command_words_timestamps[0],
        chip_select = chip_select,
      )

    elif command_function == DDR5Command_PowerDownEntry:
      on_die_termination = command_words[1][4]
      command = DDR5Command_PowerDownEntry (
        timestamp          = command_words_timestamps[0],
        chip_select        = chip_select,
        on_die_termination = on_die_termination,
      )

    elif command_function == DDR5Command_MultiPurposeCommand:
      operation = (   command_words[1][0:5]
                   ** command_words[0][5:6] )
      command = DDR5Command_MultiPurposeCommand (
        timestamp   = command_words_timestamps[0],
        chip_select = chip_select,
        operation   = operation,
      )

    return command



  def commands(self) -> Generator[DDR5Command, None, None]:
    """ Generator to iterate over all commands. """
    while True:
      next_command = self.next_command()
      if next_command:
        yield next_command
      else: return
