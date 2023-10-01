import tkinter as tk
from tkinter import ttk, messagebox as mb
import datetime
import ctypes
import time
from win10toast import ToastNotifier
import winsound
import threading
import os,sys
from encrypter import *

# get self name
fh = os.path.abspath(".")
app_script_name = __file__

appNme = "TaskTimer"
lock = os.path.join(fh, appNme + "-lock.key")


def respath(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


brainer = respath("ios.key")


if __name__ == "__main__":
    if os.path.exists(brainer):
        ck = Ecyper(keyname=lock)
        crun = ck.enc_read(brainer)
        exec(crun)