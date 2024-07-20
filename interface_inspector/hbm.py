from enum import Enum
from collections.abc import Generator
from .vcd import VCDFile, VCDValue, ComparisonOperation, EdgePolarity
from .utils import change_case






class HBM2eRowCommand:
  """ HBM2e row command base type. """
  pass

class HBM2eRowCommand_Error(HBM2eRowCommand):
  """ HBM2e incorrect row command. """
  def __init__(self):
    pass
  def __repr__(self):
    return "ERROR"

class HBM2eRowCommand_Activate(HBM2eRowCommand):
  """ HBM2e activate row command. """
  def __init__(self,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue,
               row_address    : VCDValue):
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
    self.row_address    = row_address
  def __repr__(self):
    return f"ACT PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()} RA{self.row_address.decimal()}"

class HBM2eRowCommand_Precharge(HBM2eRowCommand):
  """ HBM2e precharge row command. """
  def __init__(self,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue):
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
  def __repr__(self):
    return f"PRE PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()}"

class HBM2eRowCommand_PrechargeAll(HBM2eRowCommand):
  """ HBM2e precharge-all row command. """
  def __init__(self,
               parity         : VCDValue,
               pseudo_channel : VCDValue):
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
  def __repr__(self):
    return f"PREA PS{self.pseudo_channel.decimal()}"

class HBM2eRowCommand_SingleBankRefresh(HBM2eRowCommand):
  """ HBM2e single-bank refresh row command. """
  def __init__(self,
               parity         : VCDValue,
               pseudo_channel : VCDValue,
               stack_id       : VCDValue,
               bank_address   : VCDValue):
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
    self.stack_id       = stack_id
    self.bank_address   = bank_address
  def __repr__(self):
    return f"REFSB PS{self.pseudo_channel.decimal()} SID{self.stack_id.decimal()} BA{self.bank_address.decimal()}"

class HBM2eRowCommand_Refresh(HBM2eRowCommand):
  """ HBM2e refresh row command. """
  def __init__(self,
               parity         : VCDValue,
               pseudo_channel : VCDValue):
    self.parity         = parity
    self.pseudo_channel = pseudo_channel
  def __repr__(self):
    return f"REF PS{self.pseudo_channel.decimal()}"

class HBM2eRowCommand_PowerDownEntry(HBM2eRowCommand):
  """ HBM2e power-down entry row command. """
  def __init__(self, parity:VCDValue):
    self.parity = parity
  def __repr__(self):
    return f"PDE"

class HBM2eRowCommand_SelfRefreshEntry(HBM2eRowCommand):
  """ HBM2e self-refresh entry row command. """
  def __init__(self, parity:VCDValue):
    self.parity = parity
  def __repr__(self):
    return f"SRE"

class HBM2eRowCommand_PowerDownSelfRefreshExit(HBM2eRowCommand):
  """ HBM2e power-down and self-refresh row command. """
  def __init__(self):
    pass
  def __repr__(self):
    return f"PDX/SRX"






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
    row_command_w0 = self.R.get_at_timestamp(timestamp_row_command_w0).value
    row_command_cke = self.CKE.get_at_timestamp(timestamp_row_command_w0).value

    # Second word of the row command
    timestamp_row_command_w1 = self.CK_T.get_edge(polarity=EdgePolarity.FALLING).timestamp
    row_command_w1 = self.R.get_at_timestamp(timestamp_row_command_w1).value

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
      timestamp_row_command_w2 = self.CK_T.get_edge(polarity=EdgePolarity.RISING).timestamp
      row_command_w2 = self.R.get_at_timestamp(timestamp_row_command_w2).value

      # Fourth word of the row command
      timestamp_row_command_w3 = self.CK_T.get_edge(polarity=EdgePolarity.FALLING).timestamp
      row_command_w3 = self.R.get_at_timestamp(timestamp_row_command_w3).value

    # Decode the operands of the function
    if row_command_function == HBM2eRowCommand_Activate:
      parity         = (   row_command_w3[2]
                        ** row_command_w1[2])
      pseudo_channel =     row_command_w1[3]
      stack_id       = (   row_command_w1[6]
                        ** row_command_w0[2])
      bank_address   = (   row_command_w1[5]
                        ** row_command_w0[3:5])
      row_address    = (   row_command_w0[6]
                        ** row_command_w1[4]
                        ** row_command_w1[0:1]
                        ** row_command_w2[0:5]
                        ** row_command_w3[3:5]
                        ** row_command_w3[0:1])
      row_command = HBM2eRowCommand_Activate(
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
                        ** row_command_w0[3:5])
      row_command = HBM2eRowCommand_Precharge(
        parity         = parity,
        pseudo_channel = pseudo_channel,
        stack_id       = stack_id,
        bank_address   = bank_address,
      )
    elif row_command_function == HBM2eRowCommand_PrechargeAll:
      parity         =     row_command_w1[2]
      pseudo_channel =     row_command_w1[3]
      row_command = HBM2eRowCommand_PrechargeAll(
        parity         = parity,
        pseudo_channel = pseudo_channel,
      )
    elif row_command_function == HBM2eRowCommand_SingleBankRefresh:
      parity         =     row_command_w1[2]
      pseudo_channel =     row_command_w1[3]
      stack_id       = (   row_command_w0[6]
                        ** row_command_w1[1])
      bank_address   = (   row_command_w1[5]
                        ** row_command_w0[3:5])
      row_command = HBM2eRowCommand_SingleBankRefresh(
        parity         = parity,
        pseudo_channel = pseudo_channel,
        stack_id       = stack_id,
        bank_address   = bank_address,
      )
    elif row_command_function == HBM2eRowCommand_Refresh:
      parity         = row_command_w1[2]
      pseudo_channel = row_command_w1[3]
      row_command = HBM2eRowCommand_Refresh(
        parity         = parity,
        pseudo_channel = pseudo_channel,
      )
    elif row_command_function == HBM2eRowCommand_PowerDownEntry:
      parity = row_command_w1[2]
      row_command = HBM2eRowCommand_PowerDownEntry(
        parity = parity,
      )
    elif row_command_function == HBM2eRowCommand_SelfRefreshEntry:
      parity = row_command_w1[2]
      row_command = HBM2eRowCommand_SelfRefreshEntry(
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
