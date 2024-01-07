"""
@Author: John Mulcahy
Created Date: 2023/12/26
Last Updated: 2023/12/26
A python script to find WiFi networks & update wpa_supplicant.conf with new WiFi details
"""
import subprocess
import os
import csv
import sys

# Define general variables
wifiConf = "/etc/wpa_supplicant/wpa_supplicant.conf"
wifiUpdateFile = "wifi_update.csv"
dirPath = "/home/pi/weatherappwebsettings/"
wifiRaw = []
wifiList = []

def wifi_search():
    # Runs a terminal command to check all available WiFi networks
    result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'],
                            stdout = subprocess.PIPE)
    # Decodes and writes the terminal output to text file
    with open(dirPath+"wifiRaw.txt", "w+") as wifiFile:
        wifiFile.writelines(result.stdout.decode('utf-8'))
    # Finds just SSIDs from the available networks
    wifiFile = open(dirPath+"wifiRaw.txt", "r")
    wifiNetworks = open(dirPath+"wifiNetworkList.txt", "w+")
    wifiNetworks.writelines(["[INFO]... List of Nearby WiFi Networks \n"])
    name = "ESSID"
    while True:
        line = wifiFile.readline()
        if name in line:
            print(line)
            line = line[line.find(name):]
            if line not in wifiRaw:
                wifiRaw.append(line)
                wifiNetworks.write(line)
        if not line:
            break
    for i in wifiRaw:
        temp = i.split('"')
        wifiList.append(temp[1])
    wifiFile.close()
    wifiNetworks.close()
    return wifiList

def command_add_wifi(json):
    print("[INFO]... Checking wifi")
    # Read file WPA suppliant
    networks = []
    with open(wifiConf, "r") as f:
        inLines = f.readlines()
    # Discover existing networks
    outLines = []
    networks = []
    i = 0
    isInside = False
    for line in inLines:
        if "network={" == line.strip().replace(" ", ""):
            networks.append({})
            isInside = True
        elif "}" == line.strip().replace(" ", ""):
            i += 1
            isInside = False
        elif isInside:      
            keyValue = line.strip().split("=")
            networks[i][keyValue[0]] = keyValue[1]
        else:
            outLines.append(line)
    # Update password or add new
    isFound = False
    for network in networks:
        if network["ssid"] == f"\"{json['ssid']}\"":
            network["psk"] = f"\"{json['psk']}\""
            isFound = True
            break
    if not isFound:
        networks.append({
        'ssid': f"\"{json['ssid']}\"",
        'psk': f"\"{json['psk']}\"",
        'key_mgmt': "WPA-PSK"
        })
    # Generate new WPA Supplicant
    for network in networks:
        outLines.append("network={\n")
        for key, value in network.items():
            outLines.append(f"    {key}={value}\n")      
        outLines.append("}\n")
    cleanLines = [i for i in outLines if i != '\n']
    # Write to WPA Supplicant
    with open(wifiConf, 'w') as f:
        for line in cleanLines:
            f.write(line)
    print("[INFO]... Wifi Updated!")
