import tkinter as tk
from tkinter import ttk
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
        base_path = os.path.abspath(".") + '\\src'
        
    return os.path.join(base_path, relative_path)


App_Name = "Task Timer"
App_Icon = resource_path("favicon.ico")
App_Wavefile = resource_path("complete.wav")


class TaskTimer:    
    def __init__(self, master):
        self.master = master
        self.master.title(App_Name)
        self.master.geometry("350x100")
        self.master.resizable(False, False)
        self.master.iconbitmap(App_Icon)
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
        
    def pop_notify(self, title, msg):
        # notification.notify(
        #             title= title,
        #             message= msg,
        #             app_name= App_Name,
        #             app_icon= App_Icon,
        #             timeout=5
        #         )
        ctypes.windll.user32.MessageBoxW(None, msg, title, 0x40 | 0x1)
        
    def play_sound(self):
        ctypes.windll.winmm.mciSendStringW(f'play "{App_Wavefile}"', None, 0, None)
        
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
        start_time = datetime.datetime.now()
        total_time = target_time - start_time
        
        while self.running:
            current_time = datetime.datetime.now()
            remaining_time = target_time - current_time
            formate_remaintime = self.format_remaining_time(remaining_time)
            percentage = int((remaining_time / total_time) * 100)
            # let try to check if percentage is half of the time
            if percentage in self.reminders:
                beeptime = 2200 + percentage
                winsound.Beep(beeptime, 1000)
                self.pop_notify("Warning", f"Time's is running out you're at {percentage}%!")
                
            if remaining_time.total_seconds() <= 0:
                self.running = False
                self.log_label.config(text="Time is up!")
                winsound.Beep(2500, 2000)
                self.play_sound()
                self.reset_Timer()
                self.pop_notify("Completed", f"Time's up!")
                break
            
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
        

if __name__ == "__main__":
    root = tk.Tk()
    gui = TaskTimer(root)
    root.mainloop()
