import subprocess

def gitPull():
    print("[INFO]... Updating git software")
    result = subprocess.run(['sudo', 'sh', '/home/pi/weatherApp/gitUpdate.sh'],
                            capture_output=True,text=True)
    return result.stdout