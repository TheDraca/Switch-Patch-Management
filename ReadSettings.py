import json
import os
from platform import platform

if "Windows" in platform(): # Set ping command depending on platform
    SettingsFileLocation = (os.path.expanduser('~') + "\AppData\Roaming\SwitchPatchManagement\ " )
    CopyCommand="copy"
else:
    SettingsFileLocation = (os.path.expanduser('~') + "/.SwitchPatchManagement/ ")
    CopyCommand="cp"


SettingsFile = SettingsFileLocation.strip() + "Settings.json"


def File():
    return SettingsFileLocation.strip() + "Settings.json"

def SetupSettings():
    if os.path.exists(SettingsFileLocation) == False:
        os.mkdir(SettingsFileLocation)
    os.popen("{0} DefaultSettings.json {1}".format(CopyCommand,SettingsFile))

try:
    with open(SettingsFile) as JSONFile:
        SettingsFile = json.load(JSONFile)
except: 
    pass

def SaveSettings():
    with open(SettingsFile, 'w+') as JSONFile:
        json.dump(SettingsFile, JSONFile)

def ModifySetting(Setting, SettingName, NewValue):
    SettingsFile[Setting][SettingName] = NewValue

def RemoveSetting(Setting, SettingName):
    for i in SettingsFile[Setting][SettingName]:
        del element[i]

def AddSetting(Setting, SettingName, Value):
    SettingsFile[Setting].append(SettingName, Value)

def GetSetting(Setting, SettingName):
    return SettingsFile[Setting][SettingName]
