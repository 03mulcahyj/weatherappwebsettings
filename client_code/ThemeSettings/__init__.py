from ._anvil_designer import ThemeSettingsTemplate
from anvil import *
import anvil.server

class ThemeSettings(ThemeSettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def backButton_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('HomePage')
    print("[INFO]... Returning to HomePage")
    pass
