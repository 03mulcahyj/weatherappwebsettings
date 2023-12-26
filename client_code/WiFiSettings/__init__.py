from ._anvil_designer import WiFiSettingsTemplate
from anvil import *
import anvil.server

class WiFiSettings(WiFiSettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    wifiSSID = ['Test1','Test2','Test3']
    self.wifiDropDown.items = wifiSSID

    # Any code you write here will run before the form opens.

  def saveButton_click(self, **event_args):
    """This method is called when the button is clicked"""
    wifiSSID = self.wifiDropDown.selected_value
    wifiPassword = self.passwordBox.text
    print(wifiSSID)
    print(wifiPassword)
    pass

