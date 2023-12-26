'''
This script is to provide functions to shutdown/reboot the pi
'''
import subprocess

def shutdown():
    subprocess.call("sudo shutdown -h now", shell=True)

def reboot():
    subprocess.call("sudo reboot", shell=True)
