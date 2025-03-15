from .vcd import VCDFile, VCDValue, ComparisonOperation, EdgePolarity
from .utils import change_case






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
