import re

def change_case(string:str, upper:bool):
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

def remove_colors(string):
  """ Remove ANSI color codes from a string. """
  return re.sub(r'\x1b\[[0-9;]*m', '', string)

