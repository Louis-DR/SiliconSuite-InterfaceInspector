from dataclasses import dataclass
from enum        import Enum
from typing      import Generator

from .vcd import (
  VCDFile,
  VCDValue,
)

from .utils import (
  change_case,
  packet_string,
  Color,
)

from .packet    import Packet
from .interface import Interface






timestamp_width = 5
command_width   = 5
context_width   = 0
value_width     = 2
line_width      = 48

class APBTransaction(Packet):
  """ APB transaction base type. """
  def __str__(self):
    return self.__repr__()

class APBTransactionError(APBTransaction):
  """ APB incorrect transaction. """
  def __init__(self,
               timestamp_request  : int,
               timestamp_response : int,
               paddr              : VCDValue,
               pprot              : VCDValue,
               pnse               : VCDValue,
               pstrb              : VCDValue,
               pwdata             : VCDValue,
               prdata             : VCDValue,
               pslverr            : VCDValue):
    self.timestamp_request  = timestamp_request
    self.timestamp_response = timestamp_response
    self.paddr   = paddr
    self.pprot   = pprot
    self.pnse    = pnse
    self.pstrb   = pstrb
    self.pwdata  = pwdata
    self.prdata  = prdata
    self.pslverr = pslverr
  def __repr__(self) -> str:
    parameters = {}
    parameters["ADDR "] = self.paddr.hexadecimal()
    return packet_string(
      timestamp       = self.timestamp_request,
      command         = "ERROR",
      parameters      = parameters,
      color           = Color.BG_BLACK + Color.RED + Color.BLINK,
      timestamp_width = timestamp_width,
      command_width   = command_width,
      context_width   = context_width,
      value_width     = value_width,
      line_width      = line_width
    )

class APBTransactionRead(APBTransaction):
  """ APB read transaction. """
  def __init__(self,
               timestamp_request  : int,
               timestamp_response : int,
               paddr              : VCDValue,
               pprot              : VCDValue,
               pnse               : VCDValue,
               prdata             : VCDValue,
               pslverr            : VCDValue):
    self.timestamp_request  = timestamp_request
    self.timestamp_response = timestamp_response
    self.paddr   = paddr
    self.pprot   = pprot
    self.pnse    = pnse
    self.prdata  = prdata
    self.pslverr = pslverr
  def __repr__(self) -> str:
    parameters = {}
    parameters["ADDR "] = self.paddr.hexadecimal()
    parameters["DATA "] = self.prdata.hexadecimal()
    return packet_string(
      timestamp       = self.timestamp_request,
      command         = "READ",
      parameters      = parameters,
      color           = Color.BG_YELLOW,
      timestamp_width = timestamp_width,
      command_width   = command_width,
      context_width   = context_width,
      value_width     = value_width,
      line_width      = line_width
    )

class APBTransactionWrite(APBTransaction):
  """ APB write transaction. """
  def __init__(self,
               timestamp_request  : int,
               timestamp_response : int,
               paddr              : VCDValue,
               pprot              : VCDValue,
               pnse               : VCDValue,
               pstrb              : VCDValue,
               pwdata             : VCDValue,
               pslverr            : VCDValue):
    self.timestamp_request  = timestamp_request
    self.timestamp_response = timestamp_response
    self.paddr   = paddr
    self.pprot   = pprot
    self.pnse    = pnse
    self.pstrb   = pstrb
    self.pwdata  = pwdata
    self.pslverr = pslverr
  def __repr__(self) -> str:
    parameters = {}
    parameters["ADDR "] = self.paddr.hexadecimal()
    parameters["DATA "] = self.pwdata.hexadecimal()
    return packet_string(
      timestamp       = self.timestamp_request,
      command         = "WRITE",
      parameters      = parameters,
      color           = Color.BG_CYAN,
      timestamp_width = timestamp_width,
      command_width   = command_width,
      context_width   = context_width,
      value_width     = value_width,
      line_width      = line_width
    )






@dataclass
class APBInterfacePaths:
  """ The paths of the signals of an APB interface. """
  pclock  : str = "pclock"
  psel    : str = "psel"
  penable : str = "penable"
  pready  : str = "pready"
  paddr   : str = "paddr"
  pprot   : str = "pprot"
  pnse    : str = "pnse"
  pwrite  : str = "pwrite"
  pstrb   : str = "pstrb"
  pwdata  : str = "pwdata"
  prdata  : str = "prdata"
  pslverr : str = "pslverr"

class APBInterface(Interface):
  """ An APB interface with its VCD signals. """

  def __init__(self,
               vcd_file  : VCDFile,
               signals   : APBInterfacePaths = None,
               path      : str               = "",
               prefix    : str               = "",
               suffix    : str               = "",
               uppercase : bool              = False):
    """ Get all the signals of the APB bus. """
    if signals is None:
      self.paths   = APBInterfacePaths()
      self.pclock  = f"{path}.{prefix}{change_case('pclock',  uppercase)}{suffix}"
      self.psel    = f"{path}.{prefix}{change_case('psel',    uppercase)}{suffix}"
      self.penable = f"{path}.{prefix}{change_case('penable', uppercase)}{suffix}"
      self.pready  = f"{path}.{prefix}{change_case('pready',  uppercase)}{suffix}"
      self.paddr   = f"{path}.{prefix}{change_case('paddr',   uppercase)}{suffix}"
      self.pprot   = f"{path}.{prefix}{change_case('pprot',   uppercase)}{suffix}"
      self.pnse    = f"{path}.{prefix}{change_case('pnse',    uppercase)}{suffix}"
      self.pwrite  = f"{path}.{prefix}{change_case('pwrite',  uppercase)}{suffix}"
      self.pstrb   = f"{path}.{prefix}{change_case('pstrb',   uppercase)}{suffix}"
      self.pwdata  = f"{path}.{prefix}{change_case('pwdata',  uppercase)}{suffix}"
      self.prdata  = f"{path}.{prefix}{change_case('prdata',  uppercase)}{suffix}"
      self.pslverr = f"{path}.{prefix}{change_case('pslverr', uppercase)}{suffix}"
    else: self.paths = signals
    self.pclock  = vcd_file.get_signal( self.paths.pclock  .split('.') )
    self.psel    = vcd_file.get_signal( self.paths.psel    .split('.') )
    self.penable = vcd_file.get_signal( self.paths.penable .split('.') )
    self.pready  = vcd_file.get_signal( self.paths.pready  .split('.') )
    self.paddr   = vcd_file.get_signal( self.paths.paddr   .split('.') )
    self.pprot   = vcd_file.get_signal( self.paths.pprot   .split('.') )
    self.pnse    = vcd_file.get_signal( self.paths.pnse    .split('.') )
    self.pwrite  = vcd_file.get_signal( self.paths.pwrite  .split('.') )
    self.pstrb   = vcd_file.get_signal( self.paths.pstrb   .split('.') )
    self.pwdata  = vcd_file.get_signal( self.paths.pwdata  .split('.') )
    self.prdata  = vcd_file.get_signal( self.paths.prdata  .split('.') )
    self.pslverr = vcd_file.get_signal( self.paths.pslverr .split('.') )



  def next_transaction(self) -> APBTransaction:
    """ Get the next APB transaction. """

    # Get the timestamp of the next rising edge of the clock after assertion of penable
    sample_penable    = self.penable.get_edge(move=True)
    if sample_penable is None: return None
    timestamp_penable = sample_penable.timestamp
    timestamp_request = self.pclock.get_edge_at_timestamp(timestamp_penable, move=True).timestamp

    # Sample the request signals
    paddr   = self.paddr  .get_at_timestamp(timestamp_request).value
    pprot   = self.pprot  .get_at_timestamp(timestamp_request).value
    pwrite  = self.pwrite .get_at_timestamp(timestamp_request).value
    pstrb   = self.pstrb  .get_at_timestamp(timestamp_request).value
    pwdata  = self.pwdata .get_at_timestamp(timestamp_request).value

    # Get the timestamp of the next rising edge of the clock after assertion of pready
    pready  = self.pready .get_at_timestamp(timestamp_request, move=True).value
    timestamp_pready   = self.pready.get_edge_at_timestamp(timestamp_request, move=True).timestamp
    timestamp_response = self.pclock.get_edge_at_timestamp(timestamp_pready, move=True).timestamp

    # Sample the response signals
    prdata  = self.pprot  .get_at_timestamp(timestamp_response).value
    pslverr = self.pprot  .get_at_timestamp(timestamp_response).value

    # Sample optional signals
    pnse = None
    if self.pnse:
      pnse  = self.pnse   .get_at_timestamp(timestamp_request).value

    # Build and return the transaction object
    transaction = APBTransaction()
    if pwrite.has_xz:
      transaction = APBTransactionError(
        timestamp_request  = timestamp_request,
        timestamp_response = timestamp_response,
        paddr              = paddr,
        pprot              = pprot,
        pnse               = pnse,
        pstrb              = pstrb,
        pwdata             = pwdata,
        prdata             = prdata,
        pslverr            = pslverr,
      )
    elif pwrite:
      transaction = APBTransactionWrite(
        timestamp_request  = timestamp_request,
        timestamp_response = timestamp_response,
        paddr              = paddr,
        pprot              = pprot,
        pnse               = pnse,
        pstrb              = pstrb,
        pwdata             = pwdata,
        pslverr            = pslverr,
      )
    else:
      transaction = APBTransactionRead(
        timestamp_request  = timestamp_request,
        timestamp_response = timestamp_response,
        paddr              = paddr,
        pprot              = pprot,
        pnse               = pnse,
        prdata             = prdata,
        pslverr            = pslverr,
      )

    return transaction



  def transactions(self) -> Generator[APBTransaction, None, None]:
    """ Generator to iterate over all transactions. """
    while True:
      try:
        next_transaction = self.next_transaction()
        if next_transaction:
          yield next_transaction
        else: return
      except: return
