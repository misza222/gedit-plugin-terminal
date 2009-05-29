# -*- coding: utf-8 -*-

#  Copyright (C) 2009 - Michal Pawlowski
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

import sys
import vte
import gtk
import gedit
import subprocess

# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
        <menuitem name="Terminal" action="Terminal"/>
    </menu>
  </menubar>
</ui>
"""

class RubyConsoleWindowHelper:
  def __init__(self, plugin, window):
    print "Plugin created for", window
    self._window = window
    self._plugin = plugin
    # Insert menu items
    self._insert_menu()

  def deactivate(self):
    # Remove any installed menu items
    self._remove_menu()
    print "Plugin stopped for", self._window
    self._window = None
    self._plugin = None

  def _insert_menu(self):
    print "Menu inserted"
    # Get the GtkUIManager
    manager = self._window.get_ui_manager()
    # Create a new action group
    self._action_group = gtk.ActionGroup("RubyConsolePluginActions")
    self._action_group.add_actions([("Terminal", None, _("Terminal"),
                                     None, _("Open Terminal"),
                                     self.on_ruby_console_activate)])
    # Insert the action group
    manager.insert_action_group(self._action_group, -1)
    # Merge the UI
    self._ui_id = manager.add_ui_from_string(ui_str)
    manager.ensure_update()

  def _remove_menu(self):
    # Get the GtkUIManager
    manager = self._window.get_ui_manager()
    # Remove the ui
    manager.remove_ui(self._ui_id)
    # Remove the action group
    manager.remove_action_group(self._action_group)
    # Make sure the manager updates
    manager.ensure_update()


  # Make sure the manager updates
  def update_ui(self):
    # Called whenever the window has been updated (active tab
    # changed, etc.)
    print "Plugin update for", self._window

  # Menu activate handlers
  def on_ruby_console_activate(self, action):
    print "Menu item invoked"
    self.launch_irb()
    
  def launch_irb(self):
    b_panel = self._window.get_bottom_panel()
    
    #self.sw = gtk.ScrolledWindow()
    #self.sw.set_border_width(5)
    #self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

    self.v = vte.Terminal()
    self.v.set_size(10,10)
    self.v.set_scroll_on_output(True)
    self.v.fork_command('bash')
    
    #self.sw.add_with_viewport(self.v)
    #self.v.show()
        
    #b_panel.add_item(self.sw, 'bash', '')
    #b_panel.activate_item(self.sw)
    #b_panel.set_property("visible", True)
    b_panel.add_item(self.v, 'bash', '')
    b_panel.activate_item(self.v)
    b_panel.set_property("visible", True)

class TerminalPlugin(gedit.Plugin):
  def __init__(self):
    gedit.Plugin.__init__(self)
    self._instances = {}

  def activate(self, window):
    self._instances[window] = RubyConsoleWindowHelper(self, window)

  def deactivate(self, window):
    self._instances[window].deactivate()
    del self._instances[window]

  def update_ui(self, window):
    self._instances[window].update_ui()
