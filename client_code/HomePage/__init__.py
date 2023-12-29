from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server

class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    appDetails = anvil.server.get_app_origin()
    print("[INFO]... App URL: "+appDetails)

  def wifiSettings_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("Wifi Button pressed")
    open_form('WiFiSettings')
    pass

  def setLocation_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("Set Location Button pressed")
    open_form('SetLocation')
    pass

  def colourSettings_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("Settings Button pressed")
    open_form('Settings')
    pass

  def shutdown_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("Shutdown Button pressed")
    #Call Shutdown Function
    anvil.server.call("systemShutdown")
    pass

  def restartButton_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("Reset Button pressed")
    anvil.server.call("systemRestart")
    pass

