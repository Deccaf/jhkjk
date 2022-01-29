import shutil
import os
import getpass
import winshell
import sys
import subprocess

ROOT_DIR =  os.path.dirname(os.path.abspath(__file__))

def delete_invalid_array(array):
    rarray = []
    for el in array:
        if el != "":
            rarray.append(el)

    return rarray
            

with subprocess.Popen(["netsh", 'interface', 'show', 'interface'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
    ether_com, errors = p.communicate()
#.split('\n')[3:-2]
ether = ether_com.decode('cp866').splitlines()[3:-1]
name_of_ethernets = []
for i in range(len(ether)):
    ether_info = delete_invalid_array(ether[i].strip().split(" "))
    if ether_info[1] == "Отключен": continue
    ether_name = " ".join(ether_info[3:])
    name_of_ethernets.append(ether_name)

print("Создание...")

path = r"C:\tof"
if os.path.exists(path):
    shutil.rmtree(path)
os.makedirs(path)


path_desktop = ""
os.makedirs(path + "\launch")

print("Копирование...")

shutil.copytree("./files/WmGameAssistant", "C:/tof/WmGameAssistant")
shutil.copytree("./files/WmGpLaunch", "C:/tof/WmGpLaunch")

print("Введите путь к WmGameAssistant:")
path_to_WmGameAssistant = input()
print("Введите путь к WanmeiGameAssistant:")
path_to_WmGpLaunch = input() + "\games\HTMobile\WmGpLaunch"
print("Введите задержку для запуска (только после первого запуска):")
timeout = input()
if timeout == "":
    timeout = "30"
else:
    timeout = int(timeout)

print("Создание ярлыка для запуска на рабочем столе...")

off_ether = '\n'.join(f'netsh interface set interface "{name_of_ethernets[off]}" DISABLED' for off in range(len(name_of_ethernets)))
on_ether = '\n'.join(f'netsh interface set interface "{name_of_ethernets[off]}" ENABLED' for off in range(len(name_of_ethernets)))

text_bat = f"""@echo off
ver |>NUL find /v "5." && if "%~1"=="" (
  Echo CreateObject^("Shell.Application"^).ShellExecute WScript.Arguments^(0^),"1","","runas",1 >"%~dp0Elevating.vbs"
  cscript.exe //nologo "%~dp0Elevating.vbs" "%~f0"& goto :eof
)
@RD /S /Q "{path_to_WmGpLaunch}"
@RD /S /Q "{path_to_WmGameAssistant}"
timeout /t 5 /nobreak
md "{path_to_WmGpLaunch}"
xcopy /s "C:\\tof\WmGpLaunch" "{path_to_WmGpLaunch}"
md "{path_to_WmGameAssistant}"
xcopy /s "C:\\tof\WmGameAssistant" "{path_to_WmGameAssistant}"
{off_ether}
start /d "{path_to_WmGpLaunch}" WmgpLauncher.exe
timeout /t {timeout} /nobreak
{on_ether}"""

with open("C:/tof/launch/launch.bat", "w") as file:
    file.write(text_bat)

winshell.CreateShortcut(
    Path=os.path.join(winshell.desktop(), "Tower of Fantasy.lnk"),
    Target="C:/tof/launch/launch.bat",
    Icon=(rf"{ROOT_DIR}\files\WmGpLaunch\WmgpLauncher.exe", 0)
)

# Написано: night.
# Discord: night.#0223
# Сервер Discord разработчика: https://discord.gg/genshimpact