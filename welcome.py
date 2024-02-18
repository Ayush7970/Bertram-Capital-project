import tkinter as tk
import sqlite3
from tkinter import messagebox, simpledialog, PhotoImage
from display_page import DisplayPage

class DrinkInputPage(tk.Frame):
    def __init__(self, master, tracker):
        super().__init__(master)
        self.tracker = tracker
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.bg_image = PhotoImage(file="img__18.png")
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(self, text="Enter Drink Preferences", fg='midnight blue', bg='white',
                              font=('Bold Condensed', 50, 'bold'))
        self.label.pack(pady=120)  # Increase padding at the top


        for name in self.tracker.coworkers.keys():
            tk.Label(self, text="").pack()  # Create space between buttons
            tk.Button(self, text=f"Enter {name}'s drink", fg='midnight blue', bg='white',
                      font=('Bold Condensed', 30, 'bold'), command=lambda n=name: self.input_drink_preference(n)).pack()
        tk.Label(self, text="").pack()  # Create space at the bottom

        self.favourite_button = tk.Button(self, text="ORDER FAVOURITE DRINKs FOR EVERYONE!", fg='midnight blue', bg='white',
                                          font=('Bold Condensed', 20, 'bold'), command=self.set_favourite_drink_for_all)
        self.favourite_button.pack(pady=10)  #


        self.next_button = tk.Button(self, text="Next", fg='midnight blue', bg='black',
                                     font=('Bold Condensed', 20, 'bold'), command=self.open_display_page)
        self.next_button.pack(pady=50)  # Increase padding at the bottom

    def input_drink_preference(self, name):
        drink = simpledialog.askstring("Input", f"Enter {name}'s drink choice:", parent=self)
        if drink and drink.upper() in self.tracker.coffee_prices:
            self.tracker.coworkers[name]['drink'] = drink.upper()
            self.next_button['state'] = tk.NORMAL
        else:
            messagebox.showerror("Error",
                                 f"Invalid drink choice. Available options: {list(self.tracker.coffee_prices.keys())}")

    def open_display_page(self):
        # Clear the current frame and open the DisplayPage
        for widget in self.master.winfo_children():
            widget.destroy()
        display_page = DisplayPage(self.master, self.tracker)

    def set_favourite_drink_for_all(self):
        favourite_drink = ["CAPPUCCINO", "BLACK COFFEE", "LATTE", "ESPRESSO", "AMERICANO", "RISTRETTO", "FLAT WHITE"]
        i = 0
        for name in self.tracker.coworkers.keys():
            self.tracker.coworkers[name]['drink'] = favourite_drink[i]
            i = i + 1
        self.open_display_page()

