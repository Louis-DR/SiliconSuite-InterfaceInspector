from collections.abc import Generator
from .vcd import VCDFile, VCDValue, ComparisonOperation, EdgePolarity
from .utils import change_case






class HBM2eRowCommand:
  """ HBM2e row command base type. """
  pass

class HBM2eRowCommand_Error(HBM2eRowCommand):
  """ HBM2e incorrect row command. """
  def __init__(self, timestamp:int):
    self.timestamp = timestamp
  def __repr__(self):
    return f"[ {self.timestamp} ] ERROR"

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
    return f"[ {self.timestamp} ] ACT PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()} RA{self.row_address.decimal()}"

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
    return f"[ {self.timestamp} ] PRE PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()}"

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
    return f"[ {self.timestamp} ] PREA PS{self.pseudo_channel.decimal()}"

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
    return f"[ {self.timestamp} ] REFSB PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()}"

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
    return f"[ {self.timestamp} ] REF PS{self.pseudo_channel.decimal()}"

class HBM2eRowCommand_PowerDownEntry(HBM2eRowCommand):
  """ HBM2e power-down entry row command. """
  def __init__(self,
               timestamp : int,
               parity    : VCDValue):
    self.timestamp = timestamp
    self.parity    = parity
  def __repr__(self):
    return f"[ {self.timestamp} ] PDE"

class HBM2eRowCommand_SelfRefreshEntry(HBM2eRowCommand):
  """ HBM2e self-refresh entry row command. """
  def __init__(self,
               timestamp : int,
               parity    : VCDValue):
    self.timestamp = timestamp
    self.parity    = parity
  def __repr__(self):
    return f"[ {self.timestamp} ] SRE"

class HBM2eRowCommand_PowerDownSelfRefreshExit(HBM2eRowCommand):
  """ HBM2e power-down or self-refresh exit row command. """
  def __init__(self, timestamp:int):
    self.timestamp = timestamp
  def __repr__(self):
    return f"[ {self.timestamp} ] PDX/SRX"






class HBM2eColumnCommand:
  """ HBM2e column command base type. """
  pass

class HBM2eColumnCommand_Error(HBM2eColumnCommand):
  """ HBM2e incorrect column command. """
  def __init__(self, timestamp:int):
    self.timestamp = timestamp
  def __repr__(self):
    return f"[ {self.timestamp} ] ERROR"

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
  def __repr__(self):
    return f"[ {self.timestamp} ] RD PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()} CA{self.column_address.decimal()}"

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
  def __repr__(self):
    return f"[ {self.timestamp} ] RDA PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()} CA{self.column_address.decimal()}"

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
  def __repr__(self):
    return f"[ {self.timestamp} ] WR PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()} CA{self.column_address.decimal()}"

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
  def __repr__(self):
    return f"[ {self.timestamp} ] WRA PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()} CA{self.column_address.decimal()}"

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
    return f"[ {self.timestamp} ] MRS MR{self.mode_register.decimal()} OPb{self.operation.decimal()}"






class HBM2eInterface:
  """ An HBM2e interface with its VCD signals. """

  def __init__(self,
               vcd_file  : VCDFile,
               path      : list[str] = [],
               prefix    : str       = "",
               suffix    : str       = "",
               uppercase : bool      = True):
    """ Get all the signals of the HBM2e bus. """
    self.CK_T    = vcd_file.get_signal( path + [prefix + change_case("CK_T",   uppercase) + suffix] )
    self.CK_C    = vcd_file.get_signal( path + [prefix + change_case("CK_C",   uppercase) + suffix] )
    self.CKE     = vcd_file.get_signal( path + [prefix + change_case("CKE",    uppercase) + suffix] )
    self.C       = vcd_file.get_signal( path + [prefix + change_case("C",      uppercase) + suffix] )
    self.R       = vcd_file.get_signal( path + [prefix + change_case("R",      uppercase) + suffix] )
    self.RDQS_T  = vcd_file.get_signal( path + [prefix + change_case("RDQS_T", uppercase) + suffix] )
    self.RDQS_C  = vcd_file.get_signal( path + [prefix + change_case("RDQS_C", uppercase) + suffix] )
    self.WDQS_T  = vcd_file.get_signal( path + [prefix + change_case("WDQS_T", uppercase) + suffix] )
    self.WDQS_C  = vcd_file.get_signal( path + [prefix + change_case("WDQS_C", uppercase) + suffix] )
    self.DQ      = vcd_file.get_signal( path + [prefix + change_case("DQ",     uppercase) + suffix] )



  def next_row_command(self):
    """ Get the next HBM2e row command. """

    # Get the next non-NOP row command
    sample_R = self.R.get_edge(value=VCDValue("bxxxx111",7), comparison=ComparisonOperation.NOT_EQUAL_NO_XY, move=True)
    if sample_R is None: return None

    # First word of the row command
    timestamp_row_command_w0 = self.CK_T.get_edge_at_timestamp(sample_R.timestamp, polarity=EdgePolarity.RISING).timestamp
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
                        ** row_command_w1[2])
      pseudo_channel =     row_command_w1[3]
      stack_id       = (   row_command_w1[6]
                        ** row_command_w0[2])
      bank_address   = (   row_command_w1[5]
                        ** row_command_w0[3:6])
      row_address    = (   row_command_w0[6]
                        ** row_command_w1[4]
                        ** row_command_w1[0:2]
                        ** row_command_w2[0:6]
                        ** row_command_w3[3:6]
                        ** row_command_w3[0:2])
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
                        ** row_command_w1[1])
      bank_address   = (   row_command_w1[5]
                        ** row_command_w0[3:6])
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
                        ** row_command_w1[1])
      bank_address   = (   row_command_w1[5]
                        ** row_command_w0[3:6])
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
      next_row_command = self.next_row_command()
      if next_row_command:
        yield next_row_command
      else: return



  def next_column_command(self):
    """ Get the next HBM2e column command. """

    # Get the next non-NOP column command
    sample_C = self.C.get_edge(value=VCDValue("bxxxxxx111",9), comparison=ComparisonOperation.NOT_EQUAL_NO_XY, move=True)
    if sample_C is None: return None

    # First word of the column command
    timestamp_column_command_w0 = self.CK_T.get_edge_at_timestamp(sample_C.timestamp, polarity=EdgePolarity.RISING).timestamp
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
      bank_address   =     column_command_w0[4:8]
      column_address = (   column_command_w1[3:7]
                        ** column_command_w1[1])
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
      bank_address   =     column_command_w0[4:8]
      column_address = (   column_command_w1[3:7]
                        ** column_command_w1[1])
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
      bank_address   =     column_command_w0[4:8]
      column_address = (   column_command_w1[3:7]
                        ** column_command_w1[1])
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
      bank_address   =     column_command_w0[4:8]
      column_address = (   column_command_w1[3:7]
                        ** column_command_w1[1])
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
      mode_register =     column_command_w0[4:8]
      operation     = (   column_command_w1[3:8]
                       ** column_command_w1[0:2])
      column_command = HBM2eColumnCommand_ModeRegisterSet (
        timestamp     = timestamp_column_command_w0,
        parity        = parity,
        mode_register = mode_register,
        operation     = operation,
      )

    return column_command



  def column_commands(self) -> Generator[HBM2eColumnCommand, None, None]:
    """ Generator to iterate over all column commands. """
    while True:
      next_column_command = self.next_column_command()
      if next_column_command:
        yield next_column_command
      else: return
