#!/usr/bin/python

class KAMCPlugin:
  def __init__(self, tn, gui):
    gui.win.connect("key-release-event", self.keyrelease)
    self.tn = tn
    self.gui = gui
  
  def keyrelease(self, widget, data=None):
    keypad = { 65429 : "nw",
               65430 : "w",
               65431 : "n", 
               65432 : "e",
               65433 : "s",
               65434 : "ne",
               65435 : "se",
               65436 : "sw",
               65437 : "look"}
    if keypad.__contains__(data.keyval):
      self.tn.write(keypad[data.keyval])
      self.gui.entry.set_property("has-focus", True)


    


