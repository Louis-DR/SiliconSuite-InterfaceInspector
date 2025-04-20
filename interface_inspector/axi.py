import traceback

from dataclasses import dataclass
from enum        import Enum
from typing      import Generator

from .vcd import (
  VCDFile,
  VCDValue,
  get_value_at_timestamp_if_signal_exists,
  get_next_valid_ready_handshake_timestamp,
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
line_width      = 186

class AXITransaction(Packet):
  """ AXI transaction base type. """
  def __str__(self):
    return self.__repr__()

class AXITransactionWrite(AXITransaction):
  """ AXI write transaction. """
  def __init__(self,
               timestamp_address    : int,
               timestamp_data_first : int,
               timestamp_data_last  : int,
               timestamp_response   : int,
               identifier  : VCDValue,
               address     : VCDValue,
               length      : VCDValue,
               size        : VCDValue,
               burst       : VCDValue,
               permissions : VCDValue,
               data        : VCDValue,
               response    : VCDValue):
    self.timestamp_address    = timestamp_address
    self.timestamp_data_first = timestamp_data_first
    self.timestamp_data_last  = timestamp_data_last
    self.timestamp_response   = timestamp_response
    self.timestamp            = self.timestamp_address
    self.identifier  = identifier
    self.address     = address
    self.length      = length
    self.size        = size
    self.burst       = burst
    self.permissions = permissions
    self.data        = data
    self.response    = response
  def __repr__(self) -> str:
    parameters = {}
    parameters["ID "]   = self.identifier.hexadecimal()
    parameters["ADDR "] = self.address.hexadecimal()
    parameters["DATA "] = self.data.hexadecimal()
    return packet_string(
      timestamp       = self.timestamp,
      command         = "WRITE",
      parameters      = parameters,
      color           = Color.BG_CYAN,
      timestamp_width = timestamp_width,
      command_width   = command_width,
      context_width   = context_width,
      value_width     = value_width,
      line_width      = line_width
    )

class AXITransactionRead(AXITransaction):
  """ AXI read transaction. """
  def __init__(self,
               timestamp_address    : int,
               timestamp_data_first : int,
               timestamp_data_last  : int,
               identifier  : VCDValue,
               address     : VCDValue,
               length      : VCDValue,
               size        : VCDValue,
               burst       : VCDValue,
               permissions : VCDValue,
               data        : VCDValue,
               response    : VCDValue):
    self.timestamp_address    = timestamp_address
    self.timestamp_data_first = timestamp_data_first
    self.timestamp_data_last  = timestamp_data_last
    self.timestamp            = self.timestamp_address
    self.identifier  = identifier
    self.address     = address
    self.length      = length
    self.size        = size
    self.burst       = burst
    self.permissions = permissions
    self.data        = data
    self.response    = response
  def __repr__(self) -> str:
    parameters = {}
    parameters["ID "]   = self.identifier.hexadecimal()
    parameters["ADDR "] = self.address.hexadecimal()
    parameters["DATA "] = self.data.hexadecimal()
    return packet_string(
      timestamp       = self.timestamp,
      command         = "READ",
      parameters      = parameters,
      color           = Color.BG_YELLOW,
      timestamp_width = timestamp_width,
      command_width   = command_width,
      context_width   = context_width,
      value_width     = value_width,
      line_width      = line_width
    )






@dataclass
class AXIInterfacePaths:
  """ The paths of the signals of an AXI interface. """
  aclock  : str = "aclock"
  # Write address channel
  awid    : str = "awid"
  awaddr  : str = "awaddr"
  awlen   : str = "awlen"
  awsize  : str = "awsize"
  awburst : str = "awburst"
  awprot  : str = "awprot"
  awvalid : str = "awvalid"
  awready : str = "awready"
  # Write data channel
  wdata   : str = "wdata"
  wstrb   : str = "wstrb"
  wlast   : str = "wlast"
  wvalid  : str = "wvalid"
  wready  : str = "wready"
  # Write response channel
  bid     : str = "bid"
  bresp   : str = "bresp"
  bvalid  : str = "bvalid"
  bready  : str = "bready"
  # Read address channel
  arid    : str = "arid"
  araddr  : str = "araddr"
  arlen   : str = "arlen"
  arsize  : str = "arsize"
  arburst : str = "arburst"
  arprot  : str = "arprot"
  arvalid : str = "arvalid"
  arready : str = "arready"
  # Read data channel
  rid     : str = "rid"
  rresp   : str = "rresp"
  rdata   : str = "rdata"
  rlast   : str = "rlast"
  rvalid  : str = "rvalid"
  rready  : str = "rready"

class AXIInterface(Interface):
  """ An AXI interface with its VCD signals. """

  def __init__(self,
               vcd_file  : VCDFile,
               signals   : AXIInterfacePaths = None,
               path      : str               = "",
               prefix    : str               = "",
               suffix    : str               = "",
               uppercase : bool              = False):
    """ Get all the signals of the AXI bus. """
    if signals is None:
      self.paths   = AXIInterfacePaths()
      self.aclock  = f"{path}.{prefix}{change_case('aclock',  uppercase)}{suffix}"
      self.awid    = f"{path}.{prefix}{change_case('awid',    uppercase)}{suffix}"
      self.awaddr  = f"{path}.{prefix}{change_case('awaddr',  uppercase)}{suffix}"
      self.awlen   = f"{path}.{prefix}{change_case('awlen',   uppercase)}{suffix}"
      self.awsize  = f"{path}.{prefix}{change_case('awsize',  uppercase)}{suffix}"
      self.awburst = f"{path}.{prefix}{change_case('awburst', uppercase)}{suffix}"
      self.awprot  = f"{path}.{prefix}{change_case('awprot',  uppercase)}{suffix}"
      self.awvalid = f"{path}.{prefix}{change_case('awvalid', uppercase)}{suffix}"
      self.awready = f"{path}.{prefix}{change_case('awready', uppercase)}{suffix}"
      self.wdata   = f"{path}.{prefix}{change_case('wdata',   uppercase)}{suffix}"
      self.wstrb   = f"{path}.{prefix}{change_case('wstrb',   uppercase)}{suffix}"
      self.wlast   = f"{path}.{prefix}{change_case('wlast',   uppercase)}{suffix}"
      self.wvalid  = f"{path}.{prefix}{change_case('wvalid',  uppercase)}{suffix}"
      self.wready  = f"{path}.{prefix}{change_case('wready',  uppercase)}{suffix}"
      self.bid     = f"{path}.{prefix}{change_case('bid',     uppercase)}{suffix}"
      self.bresp   = f"{path}.{prefix}{change_case('bresp',   uppercase)}{suffix}"
      self.bvalid  = f"{path}.{prefix}{change_case('bvalid',  uppercase)}{suffix}"
      self.bready  = f"{path}.{prefix}{change_case('bready',  uppercase)}{suffix}"
      self.arid    = f"{path}.{prefix}{change_case('arid',    uppercase)}{suffix}"
      self.araddr  = f"{path}.{prefix}{change_case('araddr',  uppercase)}{suffix}"
      self.arlen   = f"{path}.{prefix}{change_case('arlen',   uppercase)}{suffix}"
      self.arsize  = f"{path}.{prefix}{change_case('arsize',  uppercase)}{suffix}"
      self.arburst = f"{path}.{prefix}{change_case('arburst', uppercase)}{suffix}"
      self.arprot  = f"{path}.{prefix}{change_case('arprot',  uppercase)}{suffix}"
      self.arvalid = f"{path}.{prefix}{change_case('arvalid', uppercase)}{suffix}"
      self.arready = f"{path}.{prefix}{change_case('arready', uppercase)}{suffix}"
      self.rid     = f"{path}.{prefix}{change_case('rid',     uppercase)}{suffix}"
      self.rresp   = f"{path}.{prefix}{change_case('rresp',   uppercase)}{suffix}"
      self.rdata   = f"{path}.{prefix}{change_case('rdata',   uppercase)}{suffix}"
      self.rlast   = f"{path}.{prefix}{change_case('rlast',   uppercase)}{suffix}"
      self.rvalid  = f"{path}.{prefix}{change_case('rvalid',  uppercase)}{suffix}"
      self.rready  = f"{path}.{prefix}{change_case('rready',  uppercase)}{suffix}"
    else: self.paths = signals
    self.aclock  = vcd_file.get_signal( self.paths.aclock  .split('.') )
    self.awid    = vcd_file.get_signal( self.paths.awid    .split('.') )
    self.awaddr  = vcd_file.get_signal( self.paths.awaddr  .split('.') )
    self.awlen   = vcd_file.get_signal( self.paths.awlen   .split('.') )
    self.awsize  = vcd_file.get_signal( self.paths.awsize  .split('.') )
    self.awburst = vcd_file.get_signal( self.paths.awburst .split('.') )
    self.awprot  = vcd_file.get_signal( self.paths.awprot  .split('.') )
    self.awvalid = vcd_file.get_signal( self.paths.awvalid .split('.') )
    self.awready = vcd_file.get_signal( self.paths.awready .split('.') )
    self.wdata   = vcd_file.get_signal( self.paths.wdata   .split('.') )
    self.wstrb   = vcd_file.get_signal( self.paths.wstrb   .split('.') )
    self.wlast   = vcd_file.get_signal( self.paths.wlast   .split('.') )
    self.wvalid  = vcd_file.get_signal( self.paths.wvalid  .split('.') )
    self.wready  = vcd_file.get_signal( self.paths.wready  .split('.') )
    self.bid     = vcd_file.get_signal( self.paths.bid     .split('.') )
    self.bresp   = vcd_file.get_signal( self.paths.bresp   .split('.') )
    self.bvalid  = vcd_file.get_signal( self.paths.bvalid  .split('.') )
    self.bready  = vcd_file.get_signal( self.paths.bready  .split('.') )
    self.arid    = vcd_file.get_signal( self.paths.arid    .split('.') )
    self.araddr  = vcd_file.get_signal( self.paths.araddr  .split('.') )
    self.arlen   = vcd_file.get_signal( self.paths.arlen   .split('.') )
    self.arsize  = vcd_file.get_signal( self.paths.arsize  .split('.') )
    self.arburst = vcd_file.get_signal( self.paths.arburst .split('.') )
    self.arprot  = vcd_file.get_signal( self.paths.arprot  .split('.') )
    self.arvalid = vcd_file.get_signal( self.paths.arvalid .split('.') )
    self.arready = vcd_file.get_signal( self.paths.arready .split('.') )
    self.rid     = vcd_file.get_signal( self.paths.rid     .split('.') )
    self.rresp   = vcd_file.get_signal( self.paths.rresp   .split('.') )
    self.rdata   = vcd_file.get_signal( self.paths.rdata   .split('.') )
    self.rlast   = vcd_file.get_signal( self.paths.rlast   .split('.') )
    self.rvalid  = vcd_file.get_signal( self.paths.rvalid  .split('.') )
    self.rready  = vcd_file.get_signal( self.paths.rready  .split('.') )



  def next_write_transaction(self) -> AXITransactionWrite:
    """ Get the next AXI write transaction. """

    # Get the timestamp of the handshake of the write address channel
    timestamp_address = get_next_valid_ready_handshake_timestamp(self.aclock, self.awvalid, self.awready)

    # Sample the address signals
    identifier  = get_value_at_timestamp_if_signal_exists(self.awid,    VCDValue.none(), timestamp=timestamp_address)
    address     = get_value_at_timestamp_if_signal_exists(self.awaddr,  VCDValue.none(), timestamp=timestamp_address)
    length      = get_value_at_timestamp_if_signal_exists(self.awlen,   VCDValue.none(), timestamp=timestamp_address)
    size        = get_value_at_timestamp_if_signal_exists(self.awsize,  VCDValue.none(), timestamp=timestamp_address)
    burst       = get_value_at_timestamp_if_signal_exists(self.awburst, VCDValue.none(), timestamp=timestamp_address)
    permissions = get_value_at_timestamp_if_signal_exists(self.awprot,  VCDValue.none(), timestamp=timestamp_address)

    # Fetch the write data beats
    timestamp_data_first = None
    timestamp_data_last  = None
    burst_data = VCDValue.none()
    for beat in range(int(length)+1):

      # Get the timestamp of the handshake of the write data channel
      timestamp_data = get_next_valid_ready_handshake_timestamp(self.aclock, self.wvalid, self.wready)

      # Sample the data signals
      strobe = get_value_at_timestamp_if_signal_exists(self.wstrb, VCDValue.none(), timestamp=timestamp_data)
      data   = get_value_at_timestamp_if_signal_exists(self.wdata, VCDValue.none(), timestamp=timestamp_data)
      last   = get_value_at_timestamp_if_signal_exists(self.wlast, VCDValue.none(), timestamp=timestamp_data)

      # Append the data to the burst
      beat_data  = data
      burst_data = beat_data ** burst_data


      # Update first and last data timestamp
      if timestamp_data_first is None:
        timestamp_data_first = timestamp_data
      if last:
        timestamp_data_last = timestamp_data


    # Get the timestamp of the handshake of the write response channel
    timestamp_response = get_next_valid_ready_handshake_timestamp(self.aclock, self.bvalid, self.bready)

    # Sample the response signals
    bid      = get_value_at_timestamp_if_signal_exists(self.bid,   VCDValue.none(), timestamp=timestamp_response)
    response = get_value_at_timestamp_if_signal_exists(self.bresp, VCDValue.none(), timestamp=timestamp_response)

    # Build and return the transaction object
    transaction = AXITransactionWrite(
      timestamp_address    = timestamp_address,
      timestamp_data_first = timestamp_data_first,
      timestamp_data_last  = timestamp_data_last,
      timestamp_response   = timestamp_response,
      identifier  = identifier,
      address     = address,
      length      = length,
      size        = size,
      burst       = burst,
      permissions = permissions,
      data        = burst_data,
      response    = response,
    )

    return transaction



  def write_transactions(self) -> Generator[AXITransactionWrite, None, None]:
    """ Generator to iterate over all write transactions. """
    while True:
      try:
        next_write_transaction = self.next_write_transaction()
        if next_write_transaction:
          yield next_write_transaction
        else: return
      except: return



  def next_read_transaction(self) -> AXITransactionRead:
    """ Get the next AXI read transaction. """

    # Get the timestamp of the handshake of the read address channel
    timestamp_address = get_next_valid_ready_handshake_timestamp(self.aclock, self.arvalid, self.arready)

    # Sample the address signals
    identifier  = get_value_at_timestamp_if_signal_exists(self.arid,    VCDValue.none(), timestamp=timestamp_address)
    address     = get_value_at_timestamp_if_signal_exists(self.araddr,  VCDValue.none(), timestamp=timestamp_address)
    length      = get_value_at_timestamp_if_signal_exists(self.arlen,   VCDValue.none(), timestamp=timestamp_address)
    size        = get_value_at_timestamp_if_signal_exists(self.arsize,  VCDValue.none(), timestamp=timestamp_address)
    burst       = get_value_at_timestamp_if_signal_exists(self.arburst, VCDValue.none(), timestamp=timestamp_address)
    permissions = get_value_at_timestamp_if_signal_exists(self.arprot,  VCDValue.none(), timestamp=timestamp_address)

    # Fetch the read data response beats
    timestamp_data_first = None
    timestamp_data_last  = None
    burst_data = VCDValue.none()
    for beat in range(int(length)+1):

      # Get the timestamp of the handshake of the read data channel
      timestamp_data = get_next_valid_ready_handshake_timestamp(self.aclock, self.rvalid, self.rready)

      # Sample the data signals
      rid      = get_value_at_timestamp_if_signal_exists(self.rid,   VCDValue.none(), timestamp=timestamp_data)
      response = get_value_at_timestamp_if_signal_exists(self.rresp, VCDValue.none(), timestamp=timestamp_data)
      data     = get_value_at_timestamp_if_signal_exists(self.rdata, VCDValue.none(), timestamp=timestamp_data)
      last     = get_value_at_timestamp_if_signal_exists(self.rlast, VCDValue.none(), timestamp=timestamp_data)

      # Append the data to the burst
      beat_data  = data
      burst_data = beat_data ** burst_data

      # Update first and last data timestamp
      if timestamp_data_first is None:
        timestamp_data_first = timestamp_data
      if last:
        timestamp_data_last = timestamp_data

    # Build and return the transaction object
    transaction = AXITransactionRead(
      timestamp_address    = timestamp_address,
      timestamp_data_first = timestamp_data_first,
      timestamp_data_last  = timestamp_data_last,
      identifier  = identifier,
      address     = address,
      length      = length,
      size        = size,
      burst       = burst,
      permissions = permissions,
      data        = burst_data,
      response    = response,
    )

    return transaction



  def read_transactions(self) -> Generator[AXITransactionRead, None, None]:
    """ Generator to iterate over all read transactions. """
    while True:
      try:
        next_read_transaction = self.next_read_transaction()
        if next_read_transaction:
          yield next_read_transaction
        else: return
      except: return
