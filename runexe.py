import os
# pyinstaller -y -i "C:/Users/mypc/Desktop/AllinOne Software/scrapper.ico" --log-level DEBUG --debug all --version-file C:/Users/mypc/Desktop/AllinOne Software/laravel.ver -m C:/Users/mypc/Desktop/AllinOne Software/manifest.manifest  ""
# enter the file name make sure all referrence files are located in same folder this runexe.py script is located
# Run runexe.py to build your .exe software

# Enter name of the .py or .spec you want to convert to .exe here
dfile = 'TaskTimer.py'
# add files or folders to include in your .exe files
# bindcmd = 'src/*'
# add files or folders to include in your .exe files
bindcmd = 'src/*'
# add .exe ico path here mostly its extension is in .ico
icos = 'src/favicon.ico'
# if you have any manifest to add, add it here or paste the full local path
manifest = 'src/TaskTimer.manifest'
# if you have any version to add, add it here or paste the full local path
version = 'src/TaskTimer.ver'
# To allow debug mode and run it via cmd to get any error log to be able to  troubleshoot it
# uncomment this debug mode if youre ready for final production without debug mode
debug = ' -w -F '
# uncomment this debug mode if you want to test in debug mode
# debug = ' -w '
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
    os.system('pyinstaller -y -c --distpath "dist2" -p "C:\DevProject\Python\Task-Timer\projectenv" --hidden-import=plyer.platforms.win.uniqueid ' + debug + icos + bindit + manifest + version + ' "' + dfile + '"')
    os.system('rmdir /S /Q build __pycache__')
    # sec = dfile.replace('.py', '.spec')
    # os.system('del ' + sec)
    print('Build successfully')
else:
    print('File does not exits ')
