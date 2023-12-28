from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.server

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def backButton_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('HomePage')
    print("[INFO]... Returning to HomePage")
    pass

  def softwareUpdate_click(self, **event_args):
    """This method is called when the button is clicked"""
    status = anvil.server.call("systemUpdate")
    if status is True:
        c = confirm("Software Updated successfully. Click Yes to reboot.")
        if c is True:
            anvil.server.call("systemRestart")
    else:
        alert("Software is up to date.")
    pass
