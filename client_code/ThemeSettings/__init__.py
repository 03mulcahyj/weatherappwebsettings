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
    open_form('Settings')
    print("[INFO]... Returning to Settings")
    pass

  def buttonRed_click(self, **event_args):
    """This method is called when the button is clicked"""
    colour = self.buttonRed.background
    print("[INFO]... Button colour is"+str(colour))
    pass

  def buttonBlue_click(self, **event_args):
    """This method is called when the button is clicked"""
    colour = self.buttonBlue.background
    print("[INFO]... Button colour is"+str(colour))
    pass

  def buttonBlack_click(self, **event_args):
    """This method is called when the button is clicked"""
    colour = self.buttonBlack.background
    print("[INFO]... Button colour is"+str(colour))
    pass

  def buttonGrey_click(self, **event_args):
    """This method is called when the button is clicked"""
    colour = self.buttonGrey.background
    print("[INFO]... Button colour is"+str(colour))
    pass


