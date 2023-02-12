import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import ctypes
import time
from plyer import notification
import winsound
import threading
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS 
    except Exception:
        # point to a folder on my local
        base_path = os.path.abspath(".") + '\\src'
        
    return os.path.join(base_path, relative_path)


class TaskTimer:    
    def __init__(self, master):
        self.app_Name = "Task Timer"
        self.app_Icon = resource_path("favicon.ico")
        self.app_Wavefile = resource_path("complete.wav")
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)
        self.master.title(self.app_Name)
        self.master.geometry("350x100")
        self.master.resizable(False, False)
        self.master.iconbitmap(self.app_Icon)
        self.running = False
        hours =  ['00'] + [str(x) for x in range(1, 25)]
        minutes = ['00'] + [str(x) for x in range(1, 61)]
        self.reminders = [51, 31, 11]
        
        self.time_label = tk.Label(self.master, text="Select timer (H:m:s):")
        self.time_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.time_hour = ttk.Combobox(self.master, state='normal', width=3, font=('Helvetica', 9), values=hours)
        self.time_hour.grid(row=0, column=1, padx=10, sticky="nsew", pady=10)
        self.time_hour.current(0)
        
        self.time_minute = ttk.Combobox(self.master, state='normal', width=3, font=('Helvetica', 9), values=minutes)
        self.time_minute.grid(row=0, column=2, padx=10, sticky="nsew", pady=10)
        self.time_minute.current(0)
        
        self.time_second = ttk.Combobox(self.master, state='normal', width=3, font=('Helvetica', 9), values=minutes)
        self.time_second.grid(row=0, column=3, padx=10, sticky="nsew", pady=10)
        self.time_second.current(0)
        
        self.start_button = tk.Button(self.master, text="Start", command=self.start, background="green", foreground='white')
        self.start_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.log_label = tk.Label(self.master, text="00:00:00", font=("TkDefaultFont", 20))
        self.log_label.grid(row=1, column=1, columnspan=4, padx=10, pady=10)
        
        # To force a GUI window to stay on top of other windows, you can use the attributes() method of the Tkinter Toplevel widget. The attributes() method is used to set various attributes of a window.
        self.master.attributes("-topmost", True)
        
    def pop_notify(self, title, msg):
        # notification.notify(
        #             title= title,
        #             message= msg,
        #             app_name= self.app_Name,
        #             app_icon= self.app_Icon,
        #             timeout=5
        #         )
        ctypes.windll.user32.MessageBoxW(None, msg, title, 0x40 | 0x1)
        
    def play_sound(self):
        ctypes.windll.winmm.mciSendStringW(f'play "{self.app_Wavefile}"', None, 0, None)
        
    def format_remaining_time(self, remaining_time):
        minutes, seconds = divmod(int(remaining_time.total_seconds()), 60)
        hours, minutes = divmod(minutes, 60)
        if hours == 0:
            return "{:0>2}m {:0>2}s".format(minutes, seconds)
        else:
            return "{:0>2}h {:0>2}m {:0>2}s".format(hours, minutes, seconds)
        
    def start(self):
        time_hour = int(self.time_hour.get())
        time_minute = int(self.time_minute.get())
        time_second = int(self.time_second.get())
        
        if not time_hour and not time_minute and not time_second:
            self.pop_notify("Error", "Please select time")
            return
        
        remaining_time = datetime.timedelta(hours=time_hour, minutes=time_minute, seconds=time_second)
        start_time = datetime.datetime.now()
        end_time = start_time + remaining_time
        
        self.start_button.config(text="Stop", command=self.stop, background="red" )
        self.time_hour.config(state="disabled")
        self.time_minute.config(state="disabled")
        self.time_second.config(state="disabled")
        
        thread = threading.Thread(target=self.start_timer, args=(end_time,), name="Timer Starter")
        thread.start()
        
    
    def start_timer(self, target_time):
        self.running = True
        self.remaining_popalert = False
        start_time = datetime.datetime.now()
        total_time = target_time - start_time
        
        while self.running:
            current_time = datetime.datetime.now()
            remaining_time = target_time - current_time
            formate_remaintime = self.format_remaining_time(remaining_time)
            percentage = int((remaining_time / total_time) * 100)
            try:
                # let try to check if percentage is half of the time
                if percentage in self.reminders:
                    if not self.remaining_popalert:
                        beeptime = 2200 + percentage
                        winsound.Beep(beeptime, 1000)
                                            
                        thread = threading.Thread(target=self.pop_notify, args=("Warning", f"Time's is running out you're at {percentage}%!",), name="Timer Notisfier")
                        thread.start()
                        self.remaining_popalert = True
                    
                else:
                    self.remaining_popalert =  False
                    
            except:
                pass
            
                
            if remaining_time.total_seconds() <= 0:
                self.running = False
                try:
                    self.log_label.config(text="Time is up!")
                    winsound.Beep(2500, 2000)
                    self.play_sound()
                    time.sleep(2)
                    self.reset_Timer()
                    self.pop_notify("Completed", f"Time's up!")
                    break
                except:
                    pass
                
            else:
                self.log_label.config(text=str(formate_remaintime))
                time.sleep(1)
            
    def stop(self):
        self.reset_Timer()
        
    def reset_Timer(self):
        self.running = False
        self.time_hour.config(state="normal")
        self.time_minute.config(state="normal")
        self.time_second.config(state="normal")
        self.time_second.config(state="normal")
        self.log_label.config(text="00:00:00")
        self.start_button.config(text="Start", command=self.start, background="green")
        
    def close_app(self):
        # messagebox.showwarning("Warning", "Are you sure you want to exit the application?")
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #     self.master.destroy()
        #     messagebox.destroy()
        self.close_all_popups()
        self.master.destroy()
        
        
    import ctypes

    def close_all_popups(self):
        try:
            # Enumerate all open windows
            EnumWindows = ctypes.windll.user32.EnumWindows
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
            GetWindowText = ctypes.windll.user32.GetWindowTextW
            GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
            IsWindowVisible = ctypes.windll.user32.IsWindowVisible

            titles = []
            def foreach_window(hwnd, lParam):
                if IsWindowVisible(hwnd):
                    length = GetWindowTextLength(hwnd)
                    buff = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buff, length + 1)
                    titles.append(buff.value)
                return True

            EnumWindows(EnumWindowsProc(foreach_window), 0)

            for title in titles:
                if "MessageBox" in title:
                    hwnd = ctypes.windll.user32.FindWindowW(None, title)
                    ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)
                    
        except Exception as e:
            print("An error occurred:", e)

        

if __name__ == "__main__":
    root = tk.Tk()
    gui = TaskTimer(root)
    root.mainloop()
