from dataclasses import dataclass
from enum import Enum
from collections.abc import Generator
from .vcd import VCDFile, VCDValue
from .utils import change_case






class APBOperation(Enum):
  """ Type of APB operation. """
  READ  = 0
  WRITE = 1
  XZ    = 2
  def __str__(self):
    return self.name



class APBTransaction:
  """ An APB read or write transaction. """

  def __init__(self,
               timestamp_request  : int,
               timestamp_response : int,
               paddr              : VCDValue,
               pprot              : VCDValue,
               pnse               : VCDValue,
               pwrite             : VCDValue,
               pstrb              : VCDValue,
               pwdata             : VCDValue,
               prdata             : VCDValue,
               pslverr            : VCDValue):
    """ Transaction with timestamps and signal values. """
    self.timestamp_request  = timestamp_request
    self.timestamp_response = timestamp_response
    self.paddr   = paddr
    self.pprot   = pprot
    self.pnse    = pnse
    self.pwrite  = pwrite
    self.pstrb   = pstrb
    self.pwdata  = pwdata
    self.prdata  = prdata
    self.pslverr = pslverr

    # Check if pwrite is X/Z, else cast to enum
    if self.pwrite.has_xz:
      self.operation = APBOperation.XZ
    else:
      self.operation = APBOperation(int(self.pwrite.value))



  def __str__(self) -> str:
    """ Display the useful information of the transaction. """
    return f"[ {self.timestamp_request} - {self.timestamp_response} ] [APB] {self.operation} @{self.paddr}"






@dataclass
class APBInterfacePaths:
  """ A set of HBM2e signal paths. """
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

class APBInterface:
  """ An APB interface with its VCD signals. """

  def __init__(self,
               vcd_file  : VCDFile,
               signals   : APBInterfacePaths = None,
               path      : str       = "",
               prefix    : str       = "",
               suffix    : str       = "",
               uppercase : bool      = False):
    """ Get all the signals of the APB bus. """
    if signals is None:
      self.paths   = APBInterface()
      self.pclock  = vcd_file.get_signal( path + [prefix + change_case("pclock", uppercase) + suffix] )
      self.psel    = vcd_file.get_signal( path + [prefix + change_case("psel",   uppercase) + suffix] )
      self.penable = vcd_file.get_signal( path + [prefix + change_case("penable",uppercase) + suffix] )
      self.pready  = vcd_file.get_signal( path + [prefix + change_case("pready", uppercase) + suffix] )
      self.paddr   = vcd_file.get_signal( path + [prefix + change_case("paddr",  uppercase) + suffix] )
      self.pprot   = vcd_file.get_signal( path + [prefix + change_case("pprot",  uppercase) + suffix] )
      self.pnse    = vcd_file.get_signal( path + [prefix + change_case("pnse",   uppercase) + suffix] )
      self.pwrite  = vcd_file.get_signal( path + [prefix + change_case("pwrite", uppercase) + suffix] )
      self.pstrb   = vcd_file.get_signal( path + [prefix + change_case("pstrb",  uppercase) + suffix] )
      self.pwdata  = vcd_file.get_signal( path + [prefix + change_case("pwdata", uppercase) + suffix] )
      self.prdata  = vcd_file.get_signal( path + [prefix + change_case("prdata", uppercase) + suffix] )
      self.pslverr = vcd_file.get_signal( path + [prefix + change_case("pslverr",uppercase) + suffix] )
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
    timestamp_request = self.pclock.get_edge_at_timestamp(timestamp_penable).timestamp

    # Sample the request signals
    paddr   = self.paddr  .get_at_timestamp(timestamp_request).value
    pprot   = self.pprot  .get_at_timestamp(timestamp_request).value
    pwrite  = self.pwrite .get_at_timestamp(timestamp_request).value
    pstrb   = self.pstrb  .get_at_timestamp(timestamp_request).value
    pwdata  = self.pwdata .get_at_timestamp(timestamp_request).value

    # Get the timestamp of the next rising edge of the clock after assertion of pready
    pready  = self.pready .get_at_timestamp(timestamp_request, move=True).value
    timestamp_pready   = self.pready.get_edge_at_timestamp(timestamp_request).timestamp
    timestamp_response = self.pclock.get_edge_at_timestamp(timestamp_pready).timestamp

    # Sample the response signals
    prdata  = self.pprot  .get_at_timestamp(timestamp_response).value
    pslverr = self.pprot  .get_at_timestamp(timestamp_response).value

    # Sample optional signals
    pnse = None
    if self.pnse:
      pnse  = self.pnse   .get_at_timestamp(timestamp_request).value

    # Build and return the transaction object
    transaction = APBTransaction(
      timestamp_request  = timestamp_request,
      timestamp_response = timestamp_response,
      paddr              = paddr,
      pprot              = pprot,
      pnse               = pnse,
      pwrite             = pwrite,
      pstrb              = pstrb,
      pwdata             = pwdata,
      prdata             = prdata,
      pslverr            = pslverr,
    )
    return transaction



  def transactions(self) -> Generator[APBTransaction, None, None]:
    """ Generator to iterate over all transactions. """
    while True:
      next_transaction = self.next_transaction()
      if next_transaction:
        yield next_transaction
      else: return
