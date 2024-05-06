import eel
import os
from PyQt5.QtWidgets import QFileDialog, QApplication
import sys
import re
import json
minecraft_directory = "C:\\Users\\Admin\\OneDrive\\Desktop\\Tutla\\CC Client\\minecraft"

client_dir = None
with open('settings.json', 'r') as file:
    settings = json.load(file)

client_dir = settings['cc_dir']
eel.init('web', allowed_extensions=['.js', '.html'])
@eel.expose
def initalize():
    global client_dir

    if client_dir==None or os.path.exists(client_dir) == False:
            mc_dir = False
            cc_dir = False
            appdata=False
            old_cc_dir = False
            if os.path.exists(os.getenv('APPDATA')):
                appdata=True 
                if os.path.exists(os.path.join(os.getenv('APPDATA'),'.minecraft')):
                    mc_dir =True
                    if os.path.exists(os.path.join(os.getenv('APPDATA'),'.minecraft/.clickcrystals')):
                        cc_dir=True
                        set_client_dir(client_dir,False)
                    elif os.path.exists(os.path.join(os.getenv('APPDATA'),'.minecraft/ClickCrystalsClient')):
                        old_cc_dir=True
                        set_client_dir(client_dir, True)

                    
            if not appdata:
                eel.launch_folder_fix("appdata folder is not found, you may be using another OS. So select a folder instead of auto detect")
            if not mc_dir:
                eel.launch_folder_fix("Minecraft folder is not found, if you are using a launcher select the ClickCrystals folder in that. Or reinstall ClickCrystals")
            if not cc_dir:
                eel.launch_folder_fix("CC folder is not found, reinstall ClickCrystals or select your ClickCrystals folder yourself.")
    log()
    
@eel.expose
def autodetect_ccfolder():
    global client_dir
    mc_dir = False
    cc_dir = False
    appdata=False
    old_cc_dir = False
    if os.path.exists(os.getenv('APPDATA')):
        appdata=True 
        if os.path.exists(os.path.join(os.getenv('APPDATA'),'.minecraft')):
            mc_dir =True
            if os.path.exists(os.path.join(os.getenv('APPDATA'),'.minecraft/.clickcrystals')):
                cc_dir=True
            elif os.path.exists(os.path.join(os.getenv('APPDATA'),'.minecraft/ClickCrystalsClient')):
                old_cc_dir=True
    if cc_dir == True: 
        client_dir = os.path.join(os.getenv('APPDATA'),'.minecraft/.clickcrystals')
@eel.expose
def ccfolderSelection():
    global client_dir
  
    app = QApplication(sys.argv)
    folder_selected = QFileDialog.getExistingDirectory(None, "Select Folder")


    if folder_selected:
        if folder_selected.lower().endswith(".clickcrystals"):
            client_dir = folder_selected
            eel.close_folder_fix()
            set_client_dir(client_dir, False)
        elif folder_selected.lower().endswith("clickcrystalsclient"):
            client_dir = folder_selected
            set_client_dir(client_dir, True)
            eel.close_folder_fix()
        else: 
            ccfolderSelection()
    
@eel.expose
def set_client_dir(dir, old): 
    global client_dir
    global settings
    client_dir=dir
    eel.close_folder_fix()
    settings['cc_dir']=client_dir

    if old:settings['old_dir']=True
    with open('settings.json', 'w') as file:
            json.dump(settings, file, indent=4)



@eel.expose
def color_code_log(lines):
    is_error = False
    is_log_end  = False
    out = ""
    for line in lines:

        if "/INFO" in line:
                    is_error=False
                    e = "<span style='color:blue'>" + line[:10] + "</span>" + line[10:]
                    #e = re.sub(r'(\S*\/INFO\S*)', r"<span style='color:gray'>\1</span><br>", e)
                    out+=e
        elif "/ERROR" in line:

                    is_error=True
                    e = "<span style='color:rgb(220,0,0)'>" + line + "</span><br>"
                    
                    out+=e
        if is_error:
                   out+= "<span style='color:rgb(220,0,0)'>" + line + "</span><br>"
    return out

def log():
    global client_dir
    

    if os.path.exists(os.path.join(client_dir,"current.log")):
        with open(os.path.join(client_dir,"current.log"),'r') as f: 
            to_log = f.readlines()
            is_error = False

            for line in to_log:

                if "/INFO" in line:
                    is_error=False
                    e = "<span style='color:blue'>" + line[:10] + "</span>" + line[10:]
                    #e = re.sub(r'(\S*\/INFO\S*)', r"<span style='color:gray'>\1</span>", e)
                    eel.log(e,"info")
                elif "/ERROR" in line:

                    is_error=True
                    e = "<span style='color:rgb(220,0,0)'>" + line + "</span>"
                    
                    eel.log(e,"info")
                if is_error:
                    eel.log("<span style='color:rgb(220,0,0)'>" + line + "</span>","info")



    else:
        eel.log('No log found, if you have a log and are seeing this check the documentation.',"error")




initalize()


eel.start('clickcrystals.html')      
