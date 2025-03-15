from dataclasses import dataclass
from .vcd import VCDFile, VCDValue, ComparisonOperation, EdgePolarity
from .utils import change_case






class DDR5Command:
  """ DDR5 command base type. """
  pass

class DDR5Command_Error(DDR5Command):
  """ DDR5 incorrect command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
  def __repr__(self):
    return f"[ {self.timestamp} ] CS{self.chip_select} ERROR"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} ACT CID{self.chip_id.decimal()} BG{self.bank_group_address.decimal()} BA{self.bank_address.decimal()} R{self.row_address.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} WRP CID{self.chip_id.decimal()} BG{self.bank_group_address.decimal()} BA{self.bank_address.decimal()} C{self.column_address.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} WRPA CID{self.chip_id.decimal()} BG{self.bank_group_address.decimal()} BA{self.bank_address.decimal()} C{self.column_address.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} MRW MRA{self.mode_register.decimal()} OP{self.operation.decimal()} CW{self.control_word.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} MRR MRA{self.mode_register.decimal()} CW{self.control_word.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} WR CID{self.chip_id.decimal()} BG{self.bank_group_address.decimal()} BA{self.bank_address.decimal()} C{self.column_address.decimal()} BL{self.burst_length.decimal()} WRP{self.partial_write.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} WRA CID{self.chip_id.decimal()} BG{self.bank_group_address.decimal()} BA{self.bank_address.decimal()} C{self.column_address.decimal()} BL{self.burst_length.decimal()} WRP{self.partial_write.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} RD CID{self.chip_id.decimal()} BG{self.bank_group_address.decimal()} BA{self.bank_address.decimal()} C{self.column_address.decimal()} BL{self.burst_length.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} RDA CID{self.chip_id.decimal()} BG{self.bank_group_address.decimal()} BA{self.bank_address.decimal()} C{self.column_address.decimal()} BL{self.burst_length.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} VrefCA OP{self.operation.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} VrefCS OP{self.operation.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} REFab CID{self.chip_id.decimal()} RIR{self.refresh_interval_rate.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} RFMab CID{self.chip_id.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} REFsb CID{self.chip_id.decimal()} BA{self.bank_address.decimal()} RIR{self.refresh_interval_rate.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} RFMsb CID{self.chip_id.decimal()} BA{self.bank_address.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} PREab CID{self.chip_id.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} PREab CID{self.chip_id.decimal()} BA{self.bank_address.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} PREpb CID{self.chip_id.decimal()} BG{self.bank_group_address.decimal()} BA{self.bank_address.decimal()}"

class DDR5Command_SelfRefreshEntry(DDR5Command):
  """ DDR5 self refresh entry command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
  def __repr__(self):
    return f"[ {self.timestamp} ] CS{self.chip_select} SRE"

class DDR5Command_SelfRefreshEntryWithFrequencyChange(DDR5Command):
  """ DDR5 self refresh entry with frequency change command. """
  def __init__(self,
               timestamp   : int,
               chip_select : VCDValue):
    self.timestamp   = timestamp
    self.chip_select = chip_select
  def __repr__(self):
    return f"[ {self.timestamp} ] CS{self.chip_select} SREF"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} PDE ODT{self.on_die_termination.decimal()}"

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
    return f"[ {self.timestamp} ] CS{self.chip_select} MPC OP{self.operation.decimal()}"






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



  def next_command(self):
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
        chip_select = chip_select_index
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
