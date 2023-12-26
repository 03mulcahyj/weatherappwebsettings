from ._anvil_designer import ThemeSettingsTemplate
from anvil import *

class ThemeSettings(ThemeSettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
