print("[INFO]... Importing standard modules")
import anvil.server
print("[INFO]... All standard modules imported")
# Custom scripts
# All of these are run by the process when it runs the server module
import shutdownCode as shutdown
import wifiCode as wifi
import updateCode as update
print("[INFO]... All custom modules imported")

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def wifiSearch():
    ''' Finds all available wifi networks'''
    print("[INFO]... Checking for broadcasting wifi networks")
    wifiList = wifi.wifi_search()
    print(wifiList)
    wifiSSID = [i for i in wifiList if i != '']
    return wifiSSID

@anvil.server.callable
def wifiUpdate(wifiDictDetails):
    ''' Takes in the wifi details in dictionary form to update them on the system'''
    print("[INFO] Updating WiFi settings")
    wifi.command_add_wifi(wifiDictDetails)
    return True

@anvil.server.callable
def systemShutdown():
    ''' Shuts down the system '''
    print("[INFO]... Shutting down the system")
    shutdown.shutdown()

@anvil.server.callable
def systemRestart():
    ''' Restarts down the system '''
    print("[INFO]... Restarting the system")
    shutdown.reboot()

@anvil.server.callable
def systemUpdate():
    ''' Updates the system with the latest code'''
    print("[INFO]... Checking for system updates")
    result = update.gitPull()
    if result == "Already up to date.":
        print("[INFO]... System is up to date")
        return False
    if ("changed" in result) or ("insertion" in result):
        print("[INFO]... GIT was updated. Pi has now been updated")
        return True

@anvil.server.callable
def themeUpdate(colour,themeSection):
    ''' Updates the theme of the weatherApp Ie Text & Background colour'''
    print("[INFO]... Updating the Theme Settings file")
    