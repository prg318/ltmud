#!/usr/bin/env python

# KAMC III
# Lukas Sabota
# ltsmooth42 _at_ gmail.com

# This is the third rewrite and it's going to be the best.  
# I'm high!

# March 30, 2009
 
import pygtk
pygtk.require("2.0")
import gtk
import sys
import vte
import gobject
import os

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

class KAMC:
    def __init__(self):
        ui = gtk.Builder()
        try:
            ui.add_from_file("kamc.glade")
        except:
            ui.add_from_file(os.path.dirname(__file__) + "/kamc.glade")
        
        callbacks = GladeCallbacks(ui, self)        
        self.ui = ui
        
        self.createMainWindow()
        gobject.timeout_add(300, self.timeout)
        
        self.tn = NetClient()

    def createMainWindow(self):
        win = gtk.Window()

        win.set_title("Kick Ass MUD Client III")
        win.set_default_size(900, 500)
        win.connect("delete_event", self.quit)
    
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        
        menu  = self.createMenu()
        vterm = self.createVterm()
        scroll_bar = gtk.VScrollbar(vterm.get_adjustment())
        scroll_bar.set_restrict_to_fill_level(True)
        entry = gtk.Entry()
        entry.connect("activate", self.enterPressed)
        vbox.pack_start(menu, expand=False)
        hbox.pack_start(vterm)
        hbox.pack_start(scroll_bar, expand=False)
        vbox.pack_start(hbox)
        vbox.pack_start(entry, expand=False)
        win.add(vbox)
        
        win.show_all()
        self.vterm = vterm
        self.mainEntry = entry
    
    def createMenu(self):
        ui_info = \
                """
                <ui>
                    <menubar name ='MenuBar'>
                        <menu action='FileMenu'>
                            <menuitem action='Connect'/>
                            <menuitem action='Disconnect'/>
                            <separator/>
                            <menuitem action='Quit'/>
                        </menu>
                        <menu action='EditMenu'>
                            <menuitem action='Preferences'/>
                        </menu>
                        <menu action='HelpMenu'>
                            <menuitem action='About'/>
                        </menu>
                    </menubar>
                </ui>
                """
        entries = (
    ( "FileMenu", None, "_File"),
    ( "Connect", gtk.STOCK_CONNECT, "C_onnect", None, None, self.connectClicked),
    ( "Disconnect", gtk.STOCK_DISCONNECT, "_Disconnect", None, None, self.disconnectClicked),
    ( "Quit", gtk.STOCK_QUIT, "_Quit", None, None, self.quit),
    ( "EditMenu", None, "_Edit"),
    ( "Preferences", gtk.STOCK_PREFERENCES, "_Preferences", None, None, self.prefsClicked),
    ( "HelpMenu", None, "_Help"),
    ( "About", gtk.STOCK_ABOUT, "_About", None, None, self.aboutClicked)
    )

        action = gtk.ActionGroup("Actions")
        action.add_actions(entries)
    
        ui = gtk.UIManager()
        ui.insert_action_group(action,0)
    
        try:
            mergeid = ui.add_ui_from_string(ui_info)
        except gobject.GError, msg:
            print "building menus failed: %s" % msg
            return None

        return ui.get_widget("/MenuBar")
        
    def connectClicked(self, widget=None, data=None):
        self.ui.get_object("connectDialog").show()
    
    def disconnectClicked(self, widget=None, data=None):
        self.tn.disconnect()
    
    def quit(self, widget=None, data=None):
        sys.exit()
    
    def prefsClicked(self, widget=None, data=None):
        self.ui.get_object("prefsDialog").show()
    
    def enterPressed(self, widget):
        self.tn.write(self.mainEntry.get_text())
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
        if not self.tn.connected:
            return True
        x = self.tn.read()
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
   
    def run(self):
        gtk.main()
        
    def aboutClicked(self, widget=None, data=None):
        response = self.ui.get_object("aboutDialog").run()
        if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CANCEL:
            self.ui.get_object("aboutDialog").hide()
    

        
    

# These are the callbacks for all of the windows and dialogs besides the
# main window.
class GladeCallbacks:
    def __init__(self, ui, parent):
        ui.connect_signals(self)
        self.ui = ui
        self.parent = parent
    
    def connect_closeClicked(self, widget, data=None):
        self.ui.get_object("connectDialog").hide()
        print 'close'
    
    def prefs_closeClicked(self, widget=None, data=None):
        self.ui.get_object("prefsDialog").hide()
    
    def prefs_delete(self, widget=None, data=None):
        self.ui.get_object("prefsDialog").hide()
        return True
        
    def quit(self, widget, data=None):
        gtk.main_quit()
        sys.exit()
    
    def connect_connectClicked(self, widget=None, data=None):
        self.parent.tn.connect(self.ui.get_object("hostEntry").get_text(),
            int(self.ui.get_object("portEntry").get_text()))
        self.ui.get_object("connectDialog").hide()
        self.parent.mainEntry.grab_focus()
    
    def connect_delete(self, widget=None, data=None):
        self.ui.get_object("connectDialog").hide()
        return True
    
    def about_delete(self, widget=None, data=None):
        self.ui.get_object("aboutDialog").hide()
        return True
        

if __name__ == "__main__":
    app = KAMC()
    app.run()

