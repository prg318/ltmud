#!/usr/bin/env python

# First run tutorial.glade through gtk-builder-convert with this command:
# gtk-builder-convert tutorial.glade tutorial.xml
# Then save this file as tutorial.py and make it executable using this command:
# chmod a+x tutorial.py
# And execute it:
# ./tutorial.py
 
import pygtk
pygtk.require("2.0")
import gtk
import sys
import vte
import gobject

class NetClient:
  def __init__(self):
    import telnetlib
    self.connected = False
    self.tn = telnetlib.Telnet()
    self.in_filters = []
    
  def disconnect(self):
    print "disconnecting"
    self.tn.close()
    self.connected = False
    
  def connect(self, host, port):
    print "connecting to ", host, port
    self.tn.open(host, port)

    print "connected..."
    self.connected = True
 
  def run_script(self, file_name):
    script = open(file_name, 'r')
    try:
      for line in script:
        self.write(line)
    finally:
      script.close()

  def read(self):
    """ read()
    This function returns a tuple: (data, status)
    If there is no data, it will return None.
    If we've been disconnected, status = -1
    """
    data = ''
    while 1:
      try:
        x = self.tn.read_eager()
      except EOFError:
        self.disconnect()
        return (data, -1)
      if x == '':
        break
      data = data + x
    
    if data == '':
      return None, 0
    return (data, 0)

  def write(self, msg):
    if self.connected:
      for x in self.in_filters:
        msg = x(msg)
      #msg = my_script(msg)
      msg = msg + '\n'
      self.tn.write(msg)

class MainWindow:
    def __init__(self):
        win = gtk.Window()

        win.set_title("Kick Ass MUD Client III")
        win.set_default_size(700, 400)
        win.connect("delete_event", self.quit)
    
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        
        #TODO
        #menu  = self.__create_menu()
        vterm = self.createVterm()
        scroll_bar = gtk.VScrollbar(vterm.get_adjustment())
        scroll_bar.set_restrict_to_fill_level(True)
        entry = gtk.Entry()
        entry.connect("activate", self.enterPressed)
    
        #vbox.pack_start(menu, expand=False)
        hbox.pack_start(vterm)
        hbox.pack_start(scroll_bar, expand=False)
        vbox.pack_start(hbox)
        vbox.pack_start(entry, expand=False)
        win.add(vbox)
        
        win.show_all()
        self.vterm = vterm
        self.mainEntry = entry
        
        gobject.timeout_add(300, self.timeout)
        #self.window = ui.get_object("mainWindow")
        #self.window.show()
        #self.dialog = ui.get_object("connectDialog")
        #self.dialog.show()
    def quit(self, widget=None, data=None):
        sys.exit()
    
    def enterPressed(self, widget):
        tn.write(self.mainEntry.get_text())
        self.mainEntry.set_property("has-focus", True)
        self.vterm.feed('\r\n')
    
    def createVterm(self):
        
        vterm = vte.Terminal()
        fg = gtk.gdk.Color(65535, 65535, 65535)
        bg = gtk.gdk.Color(0, 0, 0)
        hex_list = [
        "#000000", # black
        "#C80000", # darkred
        "#00C800", # darkblue
        "#C87D00", # orange
        "#007DC8", # darkcyan
        "#C800C8", # darkpurple
        "#00C8C8", # darkgreen 
        "#C8C8C8", # lightgrey
        "#828282", # darkgrey
        "#FF0564", # brightred
        "#64FF64", # brightgreen
        "#FFFF64", # yellow
        "#6464FF", # lightblue
        "#FF00FF", # lightpurple
        "#64FFFF", # lightcyan
        "#FFFFFF" # white
        ]

        colors = []                
        for x in hex_list:
            colors.append(gtk.gdk.color_parse(x))
    

        vterm.set_colors(fg, bg, colors)
        vterm.set_opacity(65535)
        vterm.set_scrollback_lines(1000)
    
        return vterm

    def timeout(self):
        #print "time out run"
        if not tn.connected:
            return True
        #print "connected"
        x = tn.read()
        # Redeclared for clarity
        data = x[0]
        status = x[1]
        if data:
            #print "feeding"
            self.vterm.feed(data)
        # status == 1 when disconnected
        if status == -1:
            self.displayMsg("Disconnected by remote host.")
            return True
        return True

    def displayMsg(self, string):
        string = "*** " + string + " ***"
        self.vterm.feed('\r\n')
        self.vterm.feed(string)

class KAMC2(object):       
    def __init__(self):
        ui = gtk.Builder()
        ui.add_from_file("kamc.glade")
        callbacks = GladeCallbacks(ui)
        
        # We don't use the glade-3 mainwindow because we can't use vterm
        # with it.
        #ui.get_object('mainWindow').show_all()
        self.ui = ui
        mainWindow = MainWindow()
        
        # For now, we're just displaing the connectDialog at startup.
        # When the menu is in place, this will not be the behavior.
        self.dialog = ui.get_object("connectDialog")
        self.dialog.show()

# These are the callbacks for all of the windows and dialogs besides the
# main window.
class GladeCallbacks:
    def __init__(self, ui):
        ui.connect_signals(self)
        self.ui = ui
        
    def main_connectClicked(self, widget, data=None):
        self.ui.get_object("connectDialog").show()
    
    def main_prefsClicked(self, widget, data=None):
        self.ui.get_object("prefsDialog").show()
    
    def connect_closeClicked(self, widget, data=None):
        self.ui.get_object("connectDialog").hide()
        print 'close'
    
    def prefs_closeClicked(self, widget, data=None):
        self.ui.get_object("prefsDialog").hide()
    
    def showAbout(self, widget=None, data=None):
        self.ui.get_object("aboutDialog").show()
        
    def quit(self, widget, data=None):
        gtk.main_quit()
        sys.exit()
    
    def connect_connectClicked(self, widget=None, data=None):
        tn.connect(self.ui.get_object("hostEntry").get_text(),
            int(self.ui.get_object("portEntry").get_text()))
        self.ui.get_object("connectDialog").hide()
        

if __name__ == "__main__":
  # This variable is global for now, but that's not the coolest idea.
  tn = NetClient()
  app = KAMC2()
  gtk.main()
