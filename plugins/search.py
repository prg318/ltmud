#!/usr/bin/python

class KAMCPlugin:
  def __init__(self, tn, gui):
    gui.win.connect("key-release-event", self.keyrelease)
    self.tn = tn
    self.gui = gui
  
  def keyrelease(self, widget, data=None):
    key_dict = { 65474 : "f5"}
    if key_dict.__contains__(data.keyval):
      dirs = (' ', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'u', 'd')
      for x in dirs:
        self.tn.write("search "+x)
      


    


