import tkinter as tk
from datetime import datetime, timedelta
import pygame.mixer
import time
import os

pygame.mixer.init()

def play_alarm():
    sound_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alarm.mp3')
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play()

class TimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Work & Entertainment Timer")
        self.master.geometry("400x250")

        self.time_left = timedelta()
        self.work_time = timedelta()
        self.entertainment_time = timedelta()
        self.current_mode = "stopped"
        self.prev_time = time.perf_counter()

        self.display = tk.Label(self.master, text="00:00:00", font=("Arial", 24))
        self.display.pack(pady=20)

        self.work_label = tk.Label(self.master, text="Work Time: 00:00:00", font=("Arial", 14))
        self.work_label.pack()

        self.entertainment_label = tk.Label(self.master, text="Entertainment Time: 00:00:00", font=("Arial", 14))
        self.entertainment_label.pack()

        self.start_work_button = tk.Button(self.master, text="Start Work", command=self.start_work)
        self.start_work_button.pack(fill=tk.X)

        self.start_entertainment_button = tk.Button(self.master, text="Start Entertainment", command=self.start_entertainment)
        self.start_entertainment_button.pack(fill=tk.X)

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_timer)
        self.stop_button.pack(fill=tk.X)

        self.update_timer()

    def start_work(self):
        self.current_mode = "work"
        self.prev_time = time.perf_counter()
        self.update_timer()

    def start_entertainment(self):
        self.current_mode = "entertainment"
        self.prev_time = time.perf_counter()
        self.update_timer()

    def stop_timer(self):
        self.current_mode = "stopped"

    def update_timer(self):
        current_time = time.perf_counter()
        elapsed_time = timedelta(seconds=current_time - self.prev_time)
        self.prev_time = current_time

        if self.current_mode == "work":
            self.work_time += elapsed_time
            self.time_left = self.work_time - self.entertainment_time
        elif self.current_mode == "entertainment":
            if self.entertainment_time < self.work_time:
                self.entertainment_time += elapsed_time
                self.time_left = self.work_time - self.entertainment_time
                if self.entertainment_time >= self.work_time:
                    self.entertainment_time = self.work_time
                    self.time_left = timedelta()
                    self.current_mode = "stopped"
                    play_alarm()

        if self.time_left < timedelta(seconds=0):
            self.time_left = timedelta(seconds=0)

        self.display.config(text=str(self.time_left).split(".")[0])  # Remove milliseconds from the displayed string
        self.work_label.config(text=f"Work Time: {str(self.work_time).split('.')[0]}")
        self.entertainment_label.config(text=f"Entertainment Time: {str(self.entertainment_time).split('.')[0]}")

        if self.current_mode != "stopped":
            self.master.after(10, self.update_timer)

root = tk.Tk()
app = TimerApp(root)
root.mainloop()