from enum import Enum
from .vcd import VCDFile, VCDValue
from .utils import cond_upper

class APBOperation(Enum):
  READ  = 0
  WRITE = 1
  XZ    = 2
  def __str__(self):
    return self.name

class APBTransaction:
  def __init__(self,
               timestamp_request  : int,
               timestamp_response : int,
               paddr              : VCDValue,
               pprot              : VCDValue,
               pwrite             : VCDValue,
               pstrb              : VCDValue,
               pwdata             : VCDValue,
               prdata             : VCDValue,
               pslverr            : VCDValue):
    self.timestamp_request  = timestamp_request
    self.timestamp_response = timestamp_response
    self.paddr   = paddr
    self.pprot   = pprot
    self.pwrite  = pwrite
    self.pstrb   = pstrb
    self.pwdata  = pwdata
    self.prdata  = prdata
    self.pslverr = pslverr

    if self.pwrite.has_xz:
      self.operation = APBOperation.XZ
    else:
      self.operation = APBOperation(int(self.pwrite.value))

  def __str__(self) -> str:
    return f"[ {self.timestamp_request} - {self.timestamp_response} ] [APB] {self.operation} @{self.paddr}"

class APBInterface:
  """ An APB interface with its VCD signals. """

  def __init__(self, vcd_file:VCDFile, path:list[str]=[], prefix:str="", suffix:str="",, uppercase:bool=False):
    """ Get all the signals of the APB bus. """
    self.pclock  = vcd_file.get_signal( path + [prefix + cond_upper("pclock", uppercase) + suffix] )
    self.psel    = vcd_file.get_signal( path + [prefix + cond_upper("psel",   uppercase) + suffix] )
    self.penable = vcd_file.get_signal( path + [prefix + cond_upper("penable",uppercase) + suffix] )
    self.pready  = vcd_file.get_signal( path + [prefix + cond_upper("pready", uppercase) + suffix] )
    self.paddr   = vcd_file.get_signal( path + [prefix + cond_upper("paddr",  uppercase) + suffix] )
    self.pprot   = vcd_file.get_signal( path + [prefix + cond_upper("pprot",  uppercase) + suffix] )
    self.pnse    = vcd_file.get_signal( path + [prefix + cond_upper("pnse",   uppercase) + suffix] )
    self.pwrite  = vcd_file.get_signal( path + [prefix + cond_upper("pwrite", uppercase) + suffix] )
    self.pstrb   = vcd_file.get_signal( path + [prefix + cond_upper("pstrb",  uppercase) + suffix] )
    self.pwdata  = vcd_file.get_signal( path + [prefix + cond_upper("pwdata", uppercase) + suffix] )
    self.prdata  = vcd_file.get_signal( path + [prefix + cond_upper("prdata", uppercase) + suffix] )
    self.pslverr = vcd_file.get_signal( path + [prefix + cond_upper("pslverr",uppercase) + suffix] )

  def next_transaction(self) -> APBTransaction:
    """ Get the next APB transaction. """

    # Get the timestamp of the next rising edge of the clock after assertion of penable
    timestamp_penable = self.penable.get_edge(move=True).timestamp
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
    if self.pnse:
      pnse  = self.pnse   .get_at_timestamp(timestamp_request).value

    # Build and return the transaction object
    transaction = APBTransaction(
      timestamp_request  = timestamp_request,
      timestamp_response = timestamp_response,
      paddr              = paddr,
      pprot              = pprot,
      pwrite             = pwrite,
      pstrb              = pstrb,
      pwdata             = pwdata,
      prdata             = prdata,
      pslverr            = pslverr,
    )
    return transaction
