__author__ = "Benjamin Mickler"
__copyright__ = "Copyright 2022, Benjamin Mickler"
__credits__ = ["Benjamin Mickler"]
__license__ = "GPLv3 or later"
__version__ = "220720222"
__maintainer__ = "Benjamin Mickler"
__email__ = "ben@benmickler.com"
__status__ = "Prototype"

"""
Reaction Timer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

Reaction Timer is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
Reaction Timer. If not, see <https://www.gnu.org/licenses/>.
"""

import time
import random
import sys
import threading
import tkinter as tk
import tkinter.messagebox
import platform
from help_message import HELP_MESSAGE

def moving_dash(random_time):
    start_time = time.time()
    print("\033[?25l", end="")
    while time.time() < start_time+random_time:
        print("\r -   ", end="")
        time.sleep(0.08)
        print("\r  -  ", end="")
        time.sleep(0.08)
        print("\r   - ", end="")
        time.sleep(0.08)
        print("\r    -", end="")
        time.sleep(0.1)
        print("\r   - ", end="")
        time.sleep(0.08)
        print("\r  -  ", end="")
        time.sleep(0.08)
        print("\r -   ", end="")
        time.sleep(0.08)
        print("\r-    ", end="")
        time.sleep(0.1)
    print("\033[?25h")

def start_cli_game():
    reaction_times = []
    if len(sys.argv) < 3:
        rounds = int(input("How many rounds do you want to play? "))
    else:
        rounds = int(sys.argv[2])
    for i in range(rounds):
        random_time = random.uniform(0.5, 10.0) # Generate a random floating point number between 0.5 and 10.0
        print(f"\nRound {i+1}")
        time.sleep(1)
        print("Ready")
        time.sleep(1)
        print("Set")
        time.sleep(1)
        #print("-")
        #time.sleep(random_time)
        moving_dash(random_time)
        start_time = time.time()
        input("GO")
        end_time = time.time()
        reaction_times.append(end_time - start_time)
    average = round(sum(reaction_times) / len(reaction_times), 3)
    reaction_times.sort()
    fastest = round(reaction_times[0], 3)
    slowest = round(reaction_times[-1], 3)
    print("\nReaction times:")
    print(f"Average: {average} seconds")
    print(f"Fastest: {fastest} seconds")
    print(f"Slowest: {slowest} seconds")

class gui_game:
    def __init__(self):
        """
        Set some variables, create a Tk object, create some widgets and pack() them and so on
        """
        self.awaiting_enter = False
        self.game_running = False
        self.window = tk.Tk()
        self.window.title("Reaction Timer")
        self.window.tk.call('wm', 'iconphoto', self.window._w, tk.PhotoImage(file='logo.png'))
        self.window.minsize(400, 200)
        self.window.bind("<Key>", self.handle_keypress)
        rounds_label = tk.Label(text="Rounds:")
        self.rounds_entry = tk.Entry()
        rounds_label.pack()
        self.rounds_entry.pack()
        if len(sys.argv) > 2:
            self.rounds_entry.insert(0, sys.argv[2])
        self.start_button = tk.Button(text="Start game")
        self.start_button.pack()
        self.help_button = tk.Button(text="Help", command=self.show_help_dialog)
        self.help_button.pack()
        self.start_button.bind("<Button-1>", self.start_game)
        self.label = tk.Label()
        self.label.pack()
        self.window.mainloop()
    def handle_keypress(self, event):
        """
        Called when any key is pressed. Checks key code and continues accordingly.
        """
        # Enter keycode is 36 on Linux, 13 on Windows, 2359309 or 603979789 on MacOS
        if platform.system() == "Linux":
            if self.awaiting_enter == True:
                if event.keycode == 36:
                    self.end_time = time.time()
                    self.awaiting_enter = False
            elif event.keycode in [61, 9, 43]:# Keycodes for esc, h and slash
                self.show_help_dialog()
        elif platform.system() == "Windows":
            if self.awaiting_enter == True:
                if event.keycode == 13:
                    self.end_time = time.time()
                    self.awaiting_enter = False
            elif event.keycode in [27, 191, 72]:# Keycodes for esc, h and slash
                self.show_help_dialog()
        elif platform.system() == "Darwin":
            if self.awaiting_enter == True:
                if event.keycode in [2359309, 603979789]:
                    self.end_time = time.time()
                    self.awaiting_enter = False
            elif event.keycode in [3473435, 104, 47]:# Keycodes for esc, h and slash
                self.show_help_dialog()
    def display_results(self):
        """
        Sort the reaction_times list, work out the average and set label text to results.
        """
        average = round(sum(self.reaction_times) / len(self.reaction_times), 3)
        self.reaction_times.sort()
        fastest = round(self.reaction_times[0], 3)
        slowest = round(self.reaction_times[-1], 3)
        self.label.config(text=f"Reaction times:\nAverage: {average} seconds\nFastest: {fastest} seconds\nSlowest: {slowest} seconds")
    def show_help_dialog(self):
        aboutdialog = AboutDialog(self.window)
        self.window.wait_window(aboutdialog.top)
    def rounds_to_int(self, rounds):
        try:
            rounds = int(rounds)
            return rounds
        except:
            return False
    def start_game(self, event):
        if self.game_running == False:
            rounds = self.rounds_entry.get()
            self.rounds = self.rounds_to_int(rounds)
            if self.rounds == 0 or self.rounds == False:
                tkinter.messagebox.showerror("Invalid rounds", "Please enter the number of rounds you would like to play.")
            else:
                self.reaction_times = []
                self.start_game_loop()
    def moving_dash(self, random_time):
        start_time = time.time()
        while time.time() < start_time+random_time:
            self.label.config(text=" -   ")
            time.sleep(0.08)
            self.label.config(text="  -  ")
            time.sleep(0.08)
            self.label.config(text="   - ")
            time.sleep(0.08)
            self.label.config(text="    -")
            time.sleep(0.2)
            self.label.config(text="   - ")
            time.sleep(0.08)
            self.label.config(text="  -  ")
            time.sleep(0.08)
            self.label.config(text=" -   ")
            time.sleep(0.08)
            self.label.config(text="-    ")
            time.sleep(0.2)
    def game_loop(self):
        self.start_button["state"] = "disabled"
        self.rounds_entry["state"] = "disabled"
        self.game_running = True
        for i in range(self.rounds):
            self.random_time = random.uniform(0.5, 10.0) # Generate a random floating point number between 0.5 and 10.0
            self.label.config(text=f"Round {i+1}")
            time.sleep(1)
            self.label.config(text="Ready")
            time.sleep(1)
            self.label.config(text="Set")
            time.sleep(1)
            self.moving_dash(self.random_time)
            #self.label.config(text="-")
            self.start_time = time.time()
            self.end_time = 0
            self.awaiting_enter = True
            self.label.config(text="GO")
            while self.end_time == 0:
                time.sleep(0.1)
            self.reaction_times.append(self.end_time - self.start_time)
        self.game_running = False
        self.start_button["state"] = "normal"
        self.rounds_entry["state"] = "normal"
        self.display_results()
    def start_game_loop(self):
        t = threading.Thread(target=self.game_loop, daemon = True)
        t.start()

class AboutDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.about_text = tk.Text(top)
        self.about_text.pack()
        self.about_text.config(state='normal')
        self.about_text.insert('end', HELP_MESSAGE)
        self.about_text.config(state='disabled')
        self.close_button = tk.Button(top, text='Close', command=self.top.destroy)
        self.close_button.pack()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ["-h", "--help", "help"]:
            print(HELP_MESSAGE)
            raise SystemExit
        elif sys.argv[1].lower() in ["-g", "--gui", "gui"]:
            gui_game()
        elif sys.argv[1].lower() in ["-c", "--cli", "cli"]:
            start_cli_game()
    else:
        print("Not enough arguments, use --help for help")