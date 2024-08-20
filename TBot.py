from random import uniform
from pynput.mouse import Controller, Button
from win32gui import GetWindowText, GetForegroundWindow
import pymem, pymem.process, keyboard, time, json, sys, winsound, httpx

#Globals
mouse = Controller()
isRageMode = False
IsToggled = False

#Config
try:
    with open("offsets.json", "r") as confjson: 
	    configData = json.load(confjson)
except:
    pass

#ConfigData
dwEntityList = configData["dwEntityList"]
dwLocalPlayerPawn = configData["dwLocalPlayerPawn"]
m_iIDEntIndex = configData["m_iIDEntIndex"]
m_iTeamNum = configData["m_iTeamNum"]
m_iHealth = configData["m_iHealth"]
triggerKey = configData["Keybind"]
triggerKey2 = configData["Keybind2"]

def TriggerBot(gameHandle, client, start, stop):
    player = gameHandle.read_longlong(client + dwLocalPlayerPawn)
    entityId = gameHandle.read_int(player + m_iIDEntIndex)
    
    if entityId > 0:
        entList = gameHandle.read_longlong(client + dwEntityList)
        entEntry = gameHandle.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
        entity = gameHandle.read_longlong(entEntry + 120 * (entityId & 0x1FF))
        entityTeam = gameHandle.read_int(entity + m_iTeamNum)
        playerTeam = gameHandle.read_int(player + m_iTeamNum)
        
        isHuman = 1 if (entityTeam == 2 or entityTeam == 3) else 0
        if entityTeam != playerTeam and isHuman:
            click_delay = uniform(start, stop)
            mouse.press(Button.left)
            time.sleep(click_delay)
            mouse.release(Button.left)
            time.sleep(click_delay)
    time.sleep(0.03)  

def InitializeTBot():
    global isRageMode, IsToggled
    gameHandle = pymem.Pymem("cs2.exe")
    client = pymem.process.module_from_name(gameHandle.process_handle, "client.dll").lpBaseOfDll
    
    while True:
        try:
            if not GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
                IsToggled = False
                continue

            if keyboard.is_pressed("insert"):
                if not IsToggled:
                    isRageMode = not isRageMode  
                    IsToggled = True
                    if isRageMode:
                        winsound.Beep(2500, 100)
                        winsound.Beep(2500, 100)
                    else:
                        winsound.Beep(2500, 100)                  
            else:
                IsToggled = False
    
            if isRageMode:                 
                TriggerBot(gameHandle=gameHandle, client=client, start=0.015, stop=0.03)   
            elif not isRageMode:
                if keyboard.is_pressed(triggerKey) or keyboard.is_pressed(triggerKey2):
                    TriggerBot(gameHandle=gameHandle, client=client, start=0.035, stop=0.06)             
            else:
                time.sleep(0.1)
        except KeyboardInterrupt:
            break        
        except:
            pass

if __name__ == '__main__':
    InitializeTBot()
