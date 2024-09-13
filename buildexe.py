import os
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

env_folder = os.path.join(os.path.abspath("."), 'venv')

hkey = os.path.join(app_current_folder,  dkey)
f = Ecyper(keyname=hkey)
f.create_key()
decrypted_key = f.read_key()

keyname = f.enc(dfile + '-raw.py',  dintaller)

addfiles = f",{dkey},{dintaller},src/" 

if keyname:
    dfile = dfile +'.py'
    # add files or folders to include in your .exe files
    bindcmd = 'src/favicon.ico' + addfiles
    # add .exe ico path here mostly its extension is in .ico
    icos = 'src/favicon.ico'
    # if you have any version to add, add it here or paste the full local path
    version = 'src/TaskTimer.rc'
    import_files ='win32com,plyer.platforms.win.uniqueid,plyer.platforms.win.notification,plyer.platforms.linux.notification,plyer.platforms.macosx.notification' #enter all import files seperate with commas
    # To allow debug mode and run it via cmd to get any error log to be able to  troubleshoot it
    # uncomment this debug mode if youre ready for final production without debug mode
    debug= ' -w -F' # for single buddle " -w -F" with showing command window error for debug ' -w' show command bug error  '' show errors ' -c -F' Forces the command window to appear when running the application
    command = 'pyinstaller' + debug +' -y --distpath "dist" -p "'+ env_folder +'"'

    if bindcmd:
        if ',' in bindcmd:
            x = bindcmd.split(',')
            bindit = ''
            for xx in x:
                bindit += ' --add-data "' + xx + '";"."'
        else:
            bindit = f' --add-data "{bindcmd};."'
            
        command += bindit
        
    if icos:
        command += ' -i ' + icos

    if version:
        command += ' --version-file ' + version
        
    if import_files:
        import_file = ''
        
        if ',' in import_files:
            for file in import_files.split(','):
                import_file +=' --hidden-import='+ file
        else:
            import_file +=' --hidden-import='+ import_files
            
        if 'win32com' in import_files:
            command +=' --hidden-import=win32com.client'
            command +=' --hidden-import=win32com.shell'
            command +=' --hidden-import=win32com.server'
            command +=' --hidden-import=win32com.server.localserver'
            command +=' --hidden-import=win32com.server.policy'
            command +=' --hidden-import=win32com.server.util'
            command +=' --hidden-import=win32com.server.windows'
            command +=' --hidden-import=win32com.server.dispatcher'
            command +=' --hidden-import=win32com.server.policy.policyserver'
            command +=' --hidden-import=win32com.server.policy.policyserver_proxy'
            command +=' --hidden-import=win32com.server.policy.policyserver_win32'
            
        command += import_file


    command = command +' "' + dfile + '"'
    # print(command)
    os.system(command)
    os.system('rmdir /S /Q build __pycache__')
    # os.system('del backupper.spec' )
    os.system('del '+ dkey )
    os.system('del '+ dintaller )
    print('Build successfully')

# -w (or --windowed or --noconsole):

# Hides the command window. This is typically used for GUI applications where you don't want a console window to appear.
# -F (or --onefile):

# Bundles everything into a single executable file.
# -y (or --noconfirm):

# Automatically overwrites the output directory without asking for confirmation. This is useful if you are running the command multiple times and don't want to be prompted to overwrite files.
# -c (or --console):

# Forces the command window to appear when running the application. This is the opposite of -w and is typically used for console applications where you want to see the command output.