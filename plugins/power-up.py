#!/usr/bin/python

class KAMCScript:
  def __init__(self, tn, gui):
    fail_msg = "You lost your concentration."
    spells_list = ['adrenaline control',
                   'displacement',
                   'levitation',
                   'mental barrier',
                   'thought shield',
                   'combat mind',
                   'biofeedback',
                   'enhanced strength',
                   'inertial barrier',
                   'bio-acceleration',
                   'vibrate']
    for x in spells_list:
      tn.write("cast %s" % x)
      y = tn.read()
      while y.__contains__(fail_msg):
        print "Failed!"
        tn.write("cast %s" % x)
      print "Casted!"
        


    


