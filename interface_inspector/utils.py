from typing import Dict
import re
import heapq
import subprocess

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

def command_str(timestamp:       int               = 0,
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
  """ Display a command with colors and more. """

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

def merge_command_generators(*command_generators, key=lambda command: command.timestamp):
  yield from heapq.merge(*command_generators, key=key)

def display_commands_with_pager(command_generator):
  """ Display commands in a scrollable shell pager. """
  pager = subprocess.Popen(['less', '-R', '-S'], stdin=subprocess.PIPE, text=True)
  try:
    for command in command_generator:
      pager.stdin.write(str(command)+'\n')
      pager.stdin.flush()
    pager.stdin.close()
    pager.wait()
  except BrokenPipeError:
    pass # Happens if the user quits `less` early
  except KeyboardInterrupt:
    pass # Handle Ctrl+C gracefully
