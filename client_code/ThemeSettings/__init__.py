from ._anvil_designer import ThemeSettingsTemplate
from anvil import *
import anvil.server

class ThemeSettings(ThemeSettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.ColorPicker.set_color('#ff0000')
    self._update_label()

    # Any code you write here will run before the form opens.

  def backButton_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Settings')
    print("[INFO]... Returning to Settings")
    pass

  def colorpicker_change(self, **event_args):
    self._update_label()
    
  def _update_label(self):
    self.label_1.foreground = self.ColorPicker.get_color()
