import anvil.server

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
# Custom scripts
import shutdownCode as shutdown
import wifiCode as wifi

@anvil.server.callable
def wifiSearch():
    '''
    Finds all available wifi networks
    '''
    print("[INFO]... Checking for broadcasting wifi networks")
    wifiList = wifi.wifi_search()
    print(wifiList)
    wifiSSID = [i for i in wifiList if i != '']
    return wifiSSID

@anvil.server.callable
def wifiUpdate(wifiDictDetails):
    ''' Takes in the wifi details in dictionary form to update them on the system'''
    print("Updating WiFi settings")
    wifi.command_add_wifi(wifiDictDetails)
    return True

@anvil.server.callable
def systemShutdown():
    '''
    Shuts down the system, slave then master
    '''
    print("[INFO]... Shutting down the system")
    shutdown.shutdown()

