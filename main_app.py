from exploit.restore import restore_file
from pathlib import Path
import plistlib
import traceback

running = True
passed_check = False
# tweaks
dynamic_island_enabled = False
current_model_name = ""
boot_chime_enabled = False
charge_limit_enabled = False
stage_manager_enabled = False
shutter_sound_enabled = False

gestalt_path = Path.joinpath(Path.cwd(), "com.apple.MobileGestalt.plist")

def get_ios_version(plist_path):
    with open(plist_path, 'rb') as f:
        plist = plistlib.load(f)
    
    version_string = plist.get("CacheExtra", {}).get("qNNddlUK+B/YlooNoymwgA", "")
    
    return version_string

def is_version_at_least(version_string, major, minor):
    version_parts = version_string.split('.')
    major_version = int(version_parts[0])
    minor_version = int(version_parts[1]) if len(version_parts) > 1 else 0
    
    if major_version > major:
        return True
    elif major_version == major and minor_version >= minor:
        return True
    return False

def print_option(num: int, active: bool, message: str):
    txt = str(num) + ". "
    if active:
        txt = txt + "[Y] "
    txt = txt + message
    print(txt)

while running:
    print("""\n\n\n\n
                                                                      
         ,--.                                                         
       ,--.'|                                                 ___     
   ,--,:  : |                                               ,--.'|_   
,`--.'`|  ' :         ,--,                                  |  | :,'  
|   :  :  | |       ,'_ /|  ,----._,.  ,----._,.            :  : ' :  
:   |   \\ | :  .--. |  | : /   /  ' / /   /  ' /   ,---.  .;__,'  /   
|   : '  '; |,'_ /| :  . ||   :     ||   :     |  /     \\ |  |   |    
'   ' ;.    ;|  ' | |  . .|   | .\\  .|   | .\\  . /    /  |:__,'| :    
|   | | \\   ||  | ' |  | |.   ; ';  |.   ; ';  |.    ' / |  '  : |__  
'   : |  ; .':  | : ;  ; |'   .   . |'   .   . |'   ;   /|  |  | '.'| 
|   | '`--'  '  :  `--'   \\`---`-'| | `---`-'| |'   |  / |  ;  :    ; 
'   : |      :  ,      .-./.'__/\\_: | .'__/\\_: ||   :    |  |  ,   /  
;   |.'       `--`----'    |   :    : |   :    : \\   \\  /    ---`-'   
'---'                       \\   \\  /   \\   \\  /   `----'              
                             `--`-'     `--`-'                        
    """)
    print("by LeminLimez")
    print("v1.0.1\n\n")
    
    if not passed_check and Path.exists(gestalt_path) and Path.is_file(gestalt_path):
        passed_check = True
    
    version_string = get_ios_version(gestalt_path)
    ios16orlater = is_version_at_least(version_string, 16, 0)

    if passed_check:
        if ios16orlater:
            print_option(1, dynamic_island_enabled, "Toggle Dynamic Island")
        print_option(2, current_model_name != "", "Set Device Model Name")
        print_option(3, boot_chime_enabled, "Toggle Boot Chime")
        print_option(4, charge_limit_enabled, "Toggle Charge Limit")
        print_option(5, stage_manager_enabled, "Toggle Stage Manager Supported")
        print_option(6, shutter_sound_enabled, "Disable Region Restrictions (ie. Shutter Sound)")
        print("\n9. Apply")
        print("0. Exit\n")
        page = int(input("Enter a number: "))
        if page == 1:
            dynamic_island_enabled = not dynamic_island_enabled
        elif page == 2:
            print("\n\nSet Model Name")
            print("Leave blank to turn off custom name.\n")
            name = input("Enter Model Name: ")
            current_model_name = name
        elif page == 3:
            boot_chime_enabled = not boot_chime_enabled
        elif page == 4:
            charge_limit_enabled = not charge_limit_enabled
        elif page == 5:
            stage_manager_enabled = not stage_manager_enabled
        elif page == 6:
            shutter_sound_enabled = not shutter_sound_enabled
        elif page == 9:
            print()
            # set the tweaks and apply
            # first open the file in read mode
            with open(gestalt_path, 'rb') as in_fp:
                plist = plistlib.load(in_fp)
            
            plist["CacheExtra"]["qNNddlUK+B/YlooNoymwgA"]

            # set the plist keys
            if dynamic_island_enabled and ios16orlater:
                plist["CacheExtra"]["oPeik/9e8lQWMszEjbPzng"]["ArtworkDeviceSubType"] = 2556
            if current_model_name != "":
                plist["CacheExtra"]["oPeik/9e8lQWMszEjbPzng"]["ArtworkDeviceProductDescription"] = current_model_name
            if boot_chime_enabled:
                plist["CacheExtra"]["QHxt+hGLaBPbQJbXiUJX3w"] = True
            if charge_limit_enabled:
                plist["CacheExtra"]["37NVydb//GP/GrhuTN+exg"] = True
            if stage_manager_enabled:
                plist["CacheExtra"]["qeaj75wk3HF4DwQ8qbIi7g"] = 1
            if shutter_sound_enabled:
                plist["CacheExtra"]["h63QSdBCiT/z0WU6rdQv6Q"] = "US"
                plist["CacheExtra"]["zHeENZu+wbg7PUprwNwBWg"] = "LL/A"

            # write back to the file
            with open(gestalt_path, 'wb') as out_fp:
                plistlib.dump(plist, out_fp)
            # restore to the device
            try:
                restore_file(fp=gestalt_path, restore_path="/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/Library/Caches/", restore_name="com.apple.MobileGestalt.plist")
                input("Success! Reboot your device to see the changes.")
            except Exception as e:
                print(traceback.format_exc())
                input("Press Enter to continue...")
            running = False
        elif page == 0:
            # exit the panel
            print("Goodbye!")
            running = False
    else:
        print("No MobileGestalt file found!")
        print(f"Please place the file in \'{Path.cwd()}\' with the name \'com.apple.MobileGestalt.plist\'")
        print("Remember to make a backup of the file!!\n")
        print("1. Retry")
        print("2. Enter path\n")
        choice = int(input("Enter number: "))
        if choice == 2:
            new_path = input("Enter new path to file: ")
            gestalt_path = Path(new_path)