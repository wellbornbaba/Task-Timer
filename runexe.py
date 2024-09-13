import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode, b64encode, b64decode
from encrypter import *

dfile = 'TaskTimer'

app_current_folder = os.path.abspath(".")
dkey = dfile + "-lock.key"
dintaller = "ios.key"

# Save the encrypted key to a file
env_folder = os.path.join(app_current_folder, 'projectenv')

hkey = os.path.join(app_current_folder,  dkey)
f = Ecyper(keyname=hkey)
f.create_key()
decrypted_key = f.read_key()

keyname = f.enc(dfile + '-raw.py',  dintaller)

addfiles = f",{dkey},{dintaller},src/" 

if keyname:

    # pyinstaller -y -i "C:/Users/mypc/Desktop/AllinOne Software/scrapper.ico" --log-level DEBUG --debug all --version-file C:/Users/mypc/Desktop/AllinOne Software/laravel.ver -m C:/Users/mypc/Desktop/AllinOne Software/manifest.manifest  ""
    # enter the file name make sure all referrence files are located in same folder this runexe.py script is located
    # Run runexe.py to build your .exe software

    # Enter name of the .py or .spec you want to convert to .exe here
    dfile = dfile +'.py'
    # add files or folders to include in your .exe files
    # bindcmd = 'src/*'
    # add files or folders to include in your .exe files
    # pyinstaller --onefile --add-data "path/to/plyer.platforms.win.notification.py;plyer/platforms/win" your_script.py

    bindcmd = 'src/favicon.ico' + addfiles #'src/*'
    # add .exe ico path here mostly its extension is in .ico
    icos = 'src/favicon.ico'
    # if you have any manifest to add, add it here or paste the full local path
    manifest = '' #'src/advance-file-arranger.manifest'
    # if you have any version to add, add it here or paste the full local path
    version = 'src/TaskTimer.rc'
    # To allow debug mode and run it via cmd to get any error log to be able to  troubleshoot it
    # uncomment this debug mode if youre ready for final production without debug mode
    debug = ' -w -F '
    # uncomment this debug mode if you want to test in debug mode
    debug = ' -w '
    # show error
    # debug= ' '
    if bindcmd:
        if ',' in bindcmd:
            x = bindcmd.split(',')
            bindit = ''
            for xx in x:
                bindit += ' --add-data "' + xx + '";"."'
        else:
            bindit = f' --add-data "{bindcmd};."'

    if icos:
        icos = ' -i ' + icos

    if manifest:
        manifest = ' -m ' + manifest

    if version:
        version = ' --version-file ' + version

    if dfile.endswith('spec'):
        os.system('pyinstaller --distpath "dist2" "' + dfile + '"')
        os.system('rmdir /S /Q build __pycache__')
        print('Build successfully')
        
    elif dfile:
        os.system('pyinstaller -y -c --distpath "dist2" -p "'+ env_folder +'" --hidden-import=plyer.platforms.win.uniqueid' + debug + icos + bindit + manifest + version + ' "' + dfile + '"')
        os.system('rmdir /S /Q build __pycache__')
        # sec = dfile.replace('.py', '.spec')
        os.system('del '+ dkey )
        os.system('del '+ dintaller )
        print('Build successfully')
        
    else:
        print('File does not exits ')
