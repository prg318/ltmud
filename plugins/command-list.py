#!/usr/bin/python
# Example plugin
# This is an example plugin for Kick Ass MUD Client.

ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu action="PluginMenu">
      <menuitem name="RunCommands" action="RunCommands"/>
    </menu>
  </menubar>
</ui>
"""


client = None
import gtk
# Start with this class
class KAMCPlugin:
  # KAMC will pass you the client interface, and the gui.
  # You can manipulate these directly.
  def __init__(self, tn, gui):
    entries = (
    ( "PluginMenu", None, "_Plugin"),
    ("RunCommands", None, "_Run Commands", None, None, run)
    )
    global client
    client = tn
#    action = gtk.Action("PluginMenu", "_Plugins", None, None)
#    action2 = gtk.Action('RunCommands',  "_Run Commands", None, None)
    action_group = gtk.ActionGroup("RunActionGroup")
    action_group.add_actions(entries)
    gui.ui.insert_action_group(action_group, 0)
    gui.ui.add_ui_from_string(ui_str)
    gui.ui.ensure_update()

def run(x=1, y=2):
  chooser = gtk.FileChooserDialog("Open...", None,
  gtk.FILE_CHOOSER_ACTION_OPEN,
  (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
  gtk.STOCK_OPEN, gtk.RESPONSE_OK))
  chooser.set_default_response(gtk.RESPONSE_OK)
  response = chooser.run()
  chooser.hide()
  file_name = chooser.get_filename()
  
  if file_name.lower().__contains__(".py"):
    # Here will we run the script
    y = __import__[file_name]
    y.KAMCScript(self.client, self)
  else:
    # if it's not a python file, just run the commands
    script = open(file_name, 'r')
    try:
      for line in script:
        client.write(line)
    finally:
      script.close()
  
