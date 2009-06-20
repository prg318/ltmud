#!/usr/bin/python

from string import punctuation
import gobject



class KAMCPlugin:
  def __init__(self, tn, gui):
    tn.in_filters.append(my_script)
    

def my_script(msg):
  if msg[:3].lower() == 'ooc':
    colors = {"main": "&w",
              "caps": "&W",
              "digit" : "&W",
              "punc" : "&W",
              "ooc" : "&P"}
    body = msg[4:]
    middle = ''
    for x in body:
      if x.isupper():
        middle = middle + colors["caps"] + x + colors["main"]
      elif x.isdigit():
        middle = middle + colors["digit"] + x + colors["main"]
      elif [y for y in punctuation if y == x]:
        middle = middle + colors["punc"] + x + colors["main"]
      else:
        middle = middle + x
        
    new = 'ooc ' + colors["main"] + middle + colors["ooc"]
    return new
  return msg
