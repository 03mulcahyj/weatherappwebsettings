import subprocess

def gitPull():
    print("[INFO]... Updating git software")
    result = subprocess.run(['sudo', 'sh', '/home/pi/auxilaryCode/gitUpdate.sh'],
                            capture_output=True,text=True)
    print("[INFO]... git command run. Output below:")
    print(result)
    return result.stdout