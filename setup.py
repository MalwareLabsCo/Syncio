import os
import platform

def setupSyncio():
    APPDATA = os.getenv('APPDATA')
    if "Windows".lower() not in platform.system().lower():
        exit()


    if not os.path.isdir(APPDATA+"\\Syncio"):
        os.mkdir(APPDATA+"\\Syncio")


