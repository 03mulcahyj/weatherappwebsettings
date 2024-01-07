import subprocess

def gitPull():
    print("[INFO]... Updating git software")
    if os.path.isfile('/home/pi/auxilaryCode/gitUpdate.sh') is True:
        result = subprocess.run(['sudo', 'sh', '/home/pi/auxilaryCode/gitUpdate.sh'],
                                capture_output=True,text=True)
    elif os.path.isfile('/home/pi//home/pi/weatherApp/gitUpdate.sh') is True:
        result = subprocess.run(['sudo', 'sh', '/home/pi/weatherApp/gitUpdate.sh'],
                                capture_output=True,text=True)
    print("[INFO]... git command run. Output below:")
    print(result)
    return result.stdout