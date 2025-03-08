import tkinter as tk
import time

class Stopwatch:
    def __init__(self, master):
        self.master = master
        self.master.title("Stopwatch")
        
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        
        self.label = tk.Label(master, text="00:00:00", font=("Helvetica", 48))
        self.label.pack()
        
        self.start_button = tk.Button(master, text="Start", command=self.start)
        self.start_button.pack(side="left")
        
        self.stop_button = tk.Button(master, text="Stop", command=self.stop)
        self.stop_button.pack(side="left")
        
        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.pack(side="left")
        
        self.update_clock()

    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.display_time(self.elapsed_time)
        self.master.after(100, self.update_clock)

    def display_time(self, elapsed):
        hours, remainder = divmod(int(elapsed), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def stop(self):
        if self.running:
            self.running = False

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.display_time(self.elapsed_time)

if __name__ == "__main__":
    root = tk.Tk()
    stopwatch = Stopwatch(root)
    root.mainloop()