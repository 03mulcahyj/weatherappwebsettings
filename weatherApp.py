"""
@Author: John Mulcahy
Created Date: 2023/12/10
Last Updated: 2023/12/28
A Weather App for use on Raspberry Pi

Weather Icons from: https://www.iconpacks.net/free-icon-pack/free-weather-forecast-icon-pack-201.html
  Downloaded as 32 PNG file
Code based on: https://www.youtube.com/watch?v=NCCYWIzN6hU
API setup from: https://www.tomorrow.io/blog/creating-a-gui-weather-widget-for-raspberry-pi-with-a-weather-api/
"""

from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime as dt
from string import Template
import requests
import json
import argparse
import subprocess
import os
import time
import csv

# Set Variables
#backgroundColour = "cadetblue1"
#textColour = "black"
testMode = False
internetText = ''
onlineStatus = True
internetIndicator = "green"
displayRes = "320x240" # WxH
timeList = [None] * 2
seconds_in_day = 24*60*60
dirPath = "/home/pi/weatherappwebsettings/"
# Get colour variables from file
with open("/home/pi/weatherappwebsettings/config_files/colourFile.csv") as file:
    # The file will have one row by default, and a second in the event the user updates the settings
    csv_reader = csv.DictReader(file)
    colourData = [row for row in csv_reader][-1]
    print(colourData)
backgroundColour = colourData["backgroundColour"]
textColour = colourData["textColour"]
# Get API key from file
with open("/home/pi/apiText.txt") as file:
    apiKey = file.readline()
    if "\n" in apiKey:
        apiKey = apiKey[:-1]
weatherCodeDict = {
    0: ["Unknown",dirPath+"images/weather-forecast-sign-16552.png"],
    1000: ["Clear, Sunny",dirPath+"images/yellow-sun-16526.png"],
    1100: ["Mostly Clear",dirPath+"images/yellow-sun-16526.png"],
    1101: ["Partly Cloudy",dirPath+"images/blue-cloud-and-weather-16527.png"],
    1102: ["Mostly Cloudy",dirPath+"images/blue-cloud-and-weather-16527.png"],
    1001: ["Cloudy",dirPath+"images/blue-cloud-and-weather-16527.png"],
    2000: ["Fog",dirPath+"images/cloud-fog-foggy-weather-icon-164410.jpg"],
    2100: ["Light Fog",dirPath+"images/cloud-fog-foggy-weather-icon-164410.jpg"],
    4000: ["Drizzle",dirPath+"images/rainy-and-cloudy-day-16532.png"],
    4001: ["Rain",dirPath+"images/rain-and-blue-cloud-16530.png"],
    4200: ["Light Rain",dirPath+"images/rainy-and-cloudy-day-16532.png"],
    4201: ["Heavy Rain",dirPath+"images/downpour-rainy-day-16531.png"],
    5000: ["Snow",dirPath+"images/snow-and-blue-cloud-16540.png"],
    5001: ["Flurries",dirPath+"images/snowfall-and-blue-cloud-16541.png"],
    5100: ["Light Snow",dirPath+"images/snowfall-and-blue-cloud-16541.png"],
    5101: ["Heavy Snow",dirPath+"images/snow-and-blue-cloud-16540.png"],
    6000: ["Freezing Drizzle",dirPath+"images/rainy-and-cloudy-day-16532.png"],
    6001: ["Freezing Rain",dirPath+"images/rain-and-blue-cloud-16530.png"],
    6200: ["Light Freezing Rain",dirPath+"images/rainy-and-cloudy-day-16532.png"],
    6201: ["Heavy Freezing Rain",dirPath+"images/downpour-rainy-day-16531.png"],
    7000: ["Ice Pellets",dirPath+"images/hail-and-blue-winter-cloud-16558.png"],
    7101: ["Heavy Ice Pellets",dirPath+"images/hail-weather-and-winter-cloud-16559.png"],
    7102: ["Light Ice Pellets",dirPath+"images/hail-and-blue-winter-cloud-16558.png"],
    8000: ["Thunderstorm",dirPath+"images/lightning-and-blue-rain-cloud-16533.png"]}


# Take passed inputs
parser = argparse.ArgumentParser()
parser.add_argument("--testMode","-t",action="store_true",help="Starts the script in Test Mode")
args = parser.parse_args()

if args.testMode:
    print("[INFO]... Starting in Test Mode")
    testMode = True
    internetText = "T"

def get_ip():
    command = "hostname -I"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = proc.stdout.read()
    output = output.splitlines()
    rawIP = str(output).split(' ')
    cleanIP = rawIP[0][3:]
    if len(cleanIP) > 13:
        cleanIP = "192.168.1.5"
    return cleanIP

def check_anvil_link():
    """Check that the anvil webpage is available for setting updates"""
    result = subprocess.run(['pgrep','-af','python'],
                            capture_output=True,text=True)
    if "anvil_downlink_host.run" in result.stdout:
        print("[INFO]... Anvil website is locally available")
        return True
    else:
        return True

def get_weather_data(lat,lon,apiKey):
    """Call a weather API to get the latest weather for the IP location"""
    global onlineStatus, internetIndicator
    URL = Template("https://api.tomorrow.io/v4/weather/forecast?location=$lat,$lon&apikey=$apiKey")
    if testMode is True:
        print("[INFO]... In Test Mode and using test data")
        onlineStatus = False
        internetIndicator = "yellow"
        # Opening JSON file
        with open(dirPath+'weather_data_test.json') as json_file:
            data = json.load(json_file)
            return data
    try:
        r = requests.get(url = URL.substitute(lat=lat,lon=lon,apiKey=apiKey))
        print(r)
        onlineStatus = True
        internetIndicator = "green"
        data = r.json()
        if "code" in data.keys():
            print("[INFO]... API failed - Too many calls. Using last available data")
            internetIndicator = "blue"
            # Opening JSON file
            with open(dirPath+'weather_data.json') as json_file:
                data = json.load(json_file)
                return data
        else:
            with open(dirPath+"weather_data.json", "w") as file:
                json.dump(data, file)
            return data
    except:
        print("[INFO]... Unable to connect to internet")
        onlineStatus = False
        internetIndicator = "red"
        print("[INFO]... Using last available data")
        # Opening JSON file
        with open(dirPath+'weather_data.json') as json_file:
            data = json.load(json_file)
            return data

def get_location():
    """Pull location from an IP address"""
    url = "http://ipinfo.io/json"
    try:
        r = requests.get(url) 
        data = r.json()
        loc = data["city"]
        latLong = data["loc"].split(",")
    except:
        loc = "Brighton"
        latLong = [50.8229,0.1363]
    return loc,latLong

def get_wind_direction(bearing):
    if bearing > 337.5 or bearing <= 22.5:
        windDir = "N"
        return windDir
    if bearing > 22.5 and bearing <= 67.5:
        windDir = "NE"
        return windDir
    if bearing > 67.5 and bearing <= 112.5:
        windDir = "E"
        return windDir
    if bearing > 112.5 and bearing <= 157.5:
        windDir = "SE"
        return windDir
    if bearing > 157.5 and bearing <= 202.5:
        windDir = "S"
        return windDir
    if bearing > 202.5 and bearing <= 244.5:
        windDir = "SW"
        return windDir
    if bearing > 244.5 and bearing <= 292.5:
        windDir = "W"
        return windDir
    if bearing > 292.5 and bearing <= 337.5:
        windDir = "NW"
        return windDir

def clock():
   global displayCompDTZ
   hh= dt.now().strftime("%H")
   mm= dt.now().strftime("%M")
   ss= dt.now().strftime("%S")
   displayCompDTZ.config(text= hh + ":" + mm +":" + ss,font=("Helvetica",30,"bold"),fg=textColour,bg=backgroundColour)
   displayCompDTZ.after(1000,clock)

print("[INFO]... Starting WeatherApp")

# Set display parameters & initialise app
root=tk.Tk()
root.title("WeatherApp")
root.geometry(displayRes) 
root.configure(background=backgroundColour)
root.attributes("-fullscreen",True)
root.resizable(False,False)

# Set location
print("[INFO]... Finding Location")
loc, latLong = get_location()
print("Location is:",loc)
print("Lat-Long is:",latLong)

# Display Time & Location data
locLogo = PhotoImage(file=dirPath+"images/location-16.png")
locationImage = Label(image=locLogo,bg=backgroundColour)
locationImage.place(x=160,y=160)
displayLoc = Label(text=loc,font=("Helvetica",20,"bold"),fg=textColour,bg=backgroundColour)
displayLoc.place(x=180,y=160)

valueCompTime = dt.now().strftime("%H:%M:%S")
displayCompDTZ = Label(text=valueCompTime,font=("Helvetica",30,"bold"),fg=textColour,bg=backgroundColour)
displayCompDTZ.place(x=5,y=10)

# Get Weather Data
print("[INFO]... Getting Weather Data")
print("[INFO]... Saving API Request Time")
timeList[0] = dt.now()
weatherData = get_weather_data(latLong[0],latLong[1],apiKey)

# Setup Weather data display
valueTemp = round(weatherData["timelines"]["minutely"][0]["values"]["temperature"],1)
displayTemp = Label(text=str(valueTemp)+"°C",font=("Helvetica",30,"bold"),fg=textColour,bg=backgroundColour)
displayTemp.place(x=180,y=70)

weatherCode = weatherData["timelines"]["minutely"][0]["values"]["weatherCode"]
valueDescription = weatherCodeDict[weatherCode][0]
displayDescription = Label(text=valueDescription,font=("Helvetica",15,"bold"),fg=textColour,bg=backgroundColour)
displayDescription.place(x=180,y=120)

# Set Weather Image
logoImage = PhotoImage(file=weatherCodeDict[weatherCode][1])
logo = Label(image=logoImage,bg=backgroundColour)
logo.place(x=220,y=10)

labelRainChance = Label(root,text="Chance of Rain:",font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
labelRainChance.place(x=5,y=60)
valueRainChance = weatherData["timelines"]["minutely"][0]["values"]["precipitationProbability"]
displayRainChance = Label(text=str(valueRainChance)+"%",font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
displayRainChance.place(x=130,y=60)

labelWindSpeed = Label(root,text="Wind Speed:",font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
labelWindSpeed.place(x=5,y=90)
valueWindSpeed = weatherData["timelines"]["minutely"][0]["values"]["windSpeed"]
displayWindSpeed = Label(text=valueWindSpeed,font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
displayWindSpeed.place(x=120,y=90)

labelWindDir = Label(root,text="Wind Direction:",font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
labelWindDir.place(x=5,y=120)
valueWindBearing = weatherData["timelines"]["minutely"][0]["values"]["windDirection"]
valueWindDir = get_wind_direction(valueWindBearing)
displayWindDir = Label(text=valueWindDir,font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
displayWindDir.place(x=125,y=120)

labelHumidity = Label(root,text="Humidity:",font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
labelHumidity.place(x=5,y=150)
valueHumidity = weatherData["timelines"]["minutely"][0]["values"]["humidity"]
displayHumidity = Label(text=valueHumidity,font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
displayHumidity.place(x=125,y=150)

labelPressure = Label(root,text="Pressure:",font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
labelPressure.place(x=5,y=180)
valuePressure = weatherData["timelines"]["minutely"][0]["values"]["pressureSurfaceLevel"]
displayPressure = Label(text=valuePressure,font=("Helvetica",12,"bold"),fg=textColour,bg=backgroundColour)
displayPressure.place(x=85,y=180)

# Weater Time & Internet Status indicator
valueWeatherDTZ = weatherData["timelines"]["minutely"][0]["time"].split("T")
displayWeatherDTZ = Label(text=valueWeatherDTZ[0]+" "+valueWeatherDTZ[1],font=("Helvetica",8,"bold"),fg=textColour,bg=backgroundColour)
displayWeatherDTZ.place(x=200,y=225)
labelInternet = Label(root,text=internetText,font=("Helvetica",8,"bold"),fg=textColour,bg=internetIndicator)
labelInternet.place(x=315,y=225)

ipAddress = get_ip()
if check_anvil_link() is True:
    labelIP = Label(root,text="IP: "+ipAddress+":3030",font=("Helvetica",8,"bold"),fg=textColour,bg=backgroundColour)
else:
    labelIP["text"] = "IP: "+ipAddress
labelIP.place(x=5,y=225)

# Build Tkinter Window before entering update loop
root.update()
clock()
print("[INFO]... Entering Update Loop")
while 1:
    timeList[1] = dt.now()
    difference = timeList[1] - timeList[0]
    timeElapsed = (divmod(difference.days * seconds_in_day + difference.seconds, 60)[0]*60 
                   + divmod(difference.days * seconds_in_day + difference.seconds, 60)[1])
    if timeElapsed % 5 == 0:
        print("[INFO]... Time Elapsed since last API call:",str(timeElapsed))
    time.sleep(0.1)
    if timeElapsed % 50 == 0:
        ipAddress = get_ip()
        if check_anvil_link() is True:
            labelIP["text"] = "IP: "+ipAddress+":3030"
        else:
            labelIP["text"] = "IP: "+ipAddress
    if timeElapsed > 180:
        print("[INFO]... Making API Refresh Call")
        timeList[0] = timeList[1]
        weatherData = get_weather_data(latLong[0],latLong[1],apiKey)
        valueWeatherDTZ = weatherData["timelines"]["minutely"][0]["time"].split("T")
        displayWeatherDTZ.config(text=valueWeatherDTZ[0]+" "+valueWeatherDTZ[1],font=("Helvetica",8,"bold"),fg=textColour,bg=backgroundColour)
        weatherCode = weatherData["timelines"]["minutely"][0]["values"]["weatherCode"]
        logoImage = PhotoImage(file=weatherCodeDict[weatherCode][1])
        logo["image"] = logoImage
        labelInternet["bg"] = internetIndicator
        ipAddress = get_ip()
        labelIP["text"] = "IP: "+ipAddress+":3030"
    root.update()

