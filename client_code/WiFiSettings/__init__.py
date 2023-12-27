from ._anvil_designer import WiFiSettingsTemplate
from anvil import *
import anvil.server

class WiFiSettings(WiFiSettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    wifiList = anvil.server.call("wifiSearch")
    print(wifiList)
    self.wifiDropDown.items = wifiList
    
  def saveButton_click(self, **event_args):
    """This method is called when the button is clicked"""
    ssidCheck = False
    passCheck = False
    wifiSSID = self.wifiDropDown.selected_value
    wifiPassword = self.passwordBox.text
    print(wifiSSID)
    print(wifiPassword)
    if wifiSSID is None or wifiSSID == '':
        alert("Select an SSID")
    else:
        ssidCheck = True
    if len(wifiPassword) <8:
        c = confirm("Password is less than 8 characters. Unable to use password")
    else:
        passCheck = True
    wifiDict = dict(ssid=wifiSSID,psk=wifiPassword,key_mgmt='WPA-PSK')
    print(wifiDict)
    if ssidCheck is True and passCheck is True:
        status = anvil.server.call("wifiUpdate",wifiDict)
    open_form('HomePage')
    pass

  def backButton_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('HomePage')
    pass

