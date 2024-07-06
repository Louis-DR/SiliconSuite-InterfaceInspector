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
      self.operation = APBOperation(self.pwrite.value)

  def __str__(self) -> str:
    return f"[ {self.timestamp_request} - {self.timestamp_response} ] [APB] {self.operation} @{self.paddr}"

class APBInterface:
  def __init__(self, vcd_file:VCDFile, path:list[str]=[], prefix:str="", uppercase:bool=False):
    self.pclock  = vcd_file.get_signal(path+[prefix+cond_upper("pclock", uppercase)])
    self.psel    = vcd_file.get_signal(path+[prefix+cond_upper("psel",   uppercase)])
    self.penable = vcd_file.get_signal(path+[prefix+cond_upper("penable",uppercase)])
    self.pready  = vcd_file.get_signal(path+[prefix+cond_upper("pready", uppercase)])
    self.paddr   = vcd_file.get_signal(path+[prefix+cond_upper("paddr",  uppercase)])
    self.pprot   = vcd_file.get_signal(path+[prefix+cond_upper("pprot",  uppercase)])
    self.pwrite  = vcd_file.get_signal(path+[prefix+cond_upper("pwrite", uppercase)])
    self.pstrb   = vcd_file.get_signal(path+[prefix+cond_upper("pstrb",  uppercase)])
    self.pwdata  = vcd_file.get_signal(path+[prefix+cond_upper("pwdata", uppercase)])
    self.prdata  = vcd_file.get_signal(path+[prefix+cond_upper("prdata", uppercase)])
    self.pslverr = vcd_file.get_signal(path+[prefix+cond_upper("pslverr",uppercase)])

  def next_transaction(self) -> APBTransaction:
    timestamp_penable = self.penable.get_edge(move=True).timestamp
    timestamp_request = self.pclock.get_edge_at_timestamp(timestamp_penable).timestamp
    paddr   = self.paddr  .get_at_timestamp(timestamp_request).value
    pprot   = self.pprot  .get_at_timestamp(timestamp_request).value
    pwrite  = self.pwrite .get_at_timestamp(timestamp_request).value
    pstrb   = self.pstrb  .get_at_timestamp(timestamp_request).value
    pwdata  = self.pwdata .get_at_timestamp(timestamp_request).value
    pready  = self.pready .get_at_timestamp(timestamp_request, move=True).value
    timestamp_response = self.pready.get_edge_at_timestamp(timestamp_request).timestamp
    prdata  = self.pprot  .get_at_timestamp(timestamp_response).value
    pslverr = self.pprot  .get_at_timestamp(timestamp_response).value
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
