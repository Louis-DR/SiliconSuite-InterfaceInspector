import re
import heapq
import subprocess

from typing import (
  Dict,
  Generator,
  Callable,
)

from .packet import Packet
from .annotator import Annotator






def change_case(string:str, upper:bool) -> str:
  if upper: return string.upper()
  else:     return string.lower()



class Color:
  """ Helper class with ANSI color codes. """

  RESET      = '\033[0m'
  BOLD       = "\033[1m"
  FAINT      = "\033[2m"
  ITALIC     = "\033[3m"
  UNDERLINE  = "\033[4m"
  BLINK      = "\033[5m"
  NEGATIVE   = "\033[7m"
  CROSSED    = "\033[9m"

  BLACK      = '\033[30m'
  RED        = '\033[31m'
  GREEN      = '\033[32m'
  YELLOW     = '\033[33m'
  BLUE       = '\033[34m'
  MAGENTA    = '\033[35m'
  CYAN       = '\033[36m'
  WHITE      = '\033[37m'
  DEFAULT    = '\033[39m'

  BG_BLACK   = '\033[40m'
  BG_RED     = '\033[41m'
  BG_GREEN   = '\033[42m'
  BG_YELLOW  = '\033[43m'
  BG_BLUE    = '\033[44m'
  BG_MAGENTA = '\033[45m'
  BG_CYAN    = '\033[46m'
  BG_WHITE   = '\033[47m'
  BG_DEFAULT = '\033[49m'

def remove_colors(string:str) -> str:
  """ Remove ANSI color codes from a string. """
  return re.sub(r'\x1b\[[0-9;]*m', '', string)



def packet_string(timestamp:       int               = 0,
                  command:         str               = "NOP",
                  parameters:      Dict[str,str|int] = {},
                  context:         str               = None,
                  color:           Color|str         = None,
                  timestamp_width: int               = 0,
                  context_width:   int               = 0,
                  command_width:   int               = 5,
                  value_width:     int               = 2,
                  line_width:      int               = 50
                  ) -> str:
  """ Display a packet with colors and more. """

  string = ""

  string += Color.BLACK
  string += Color.BG_WHITE
  string += Color.BOLD
  string += f"[ {timestamp:>{timestamp_width}} ]"
  string += Color.RESET

  if context is not None:
    string += Color.WHITE
    string += color
    string += " "
    string += context.ljust(context_width)
    string += Color.RESET

  string += Color.BOLD
  string += Color.WHITE
  string += color
  string += " "
  string += command.ljust(command_width)
  string += " "
  string += Color.RESET

  string += Color.WHITE
  string += color
  for parameter, value in parameters.items():
    string += parameter
    string += str(value).ljust(value_width)
    string += " "

  string += " " * (line_width - len(remove_colors(string)))
  string += Color.RESET

  return string



def merge_packet_generators(*packet_generators : Generator[Packet, None, None], key : Callable[[Packet], int] = lambda command: command.timestamp) -> Generator[Packet, None, None]:
  yield from heapq.merge(*packet_generators, key=key)

def packet_and_annotator_generator(packet_generator:Generator[Packet, None, None], *annotators:Annotator) -> Generator[str, None, None]:
  for packet in packet_generator:
    for annotator in annotators:
      annotator.update(packet)
    yield repr(packet) + "  " + " ".join(repr(annotator) for annotator in annotators)



def display_packets_with_pager(packet_generator:Generator[Packet|str, None, None]) -> None:
  """ Display packets in a scrollable shell pager. """
  pager = subprocess.Popen(['less', '-R', '-S', '-#', '8'], stdin=subprocess.PIPE, text=True)
  try:
    for packet in packet_generator:
      pager.stdin.write(str(packet)+'\n')
      pager.stdin.flush()
    pager.stdin.close()
    pager.wait()
  except BrokenPipeError:
    pass # Happens if the user quits `less` early
  except KeyboardInterrupt:
    pass # Handle Ctrl+C gracefully
