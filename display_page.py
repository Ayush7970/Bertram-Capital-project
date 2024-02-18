import tkinter as tk
from tkinter import messagebox, PhotoImage

# Assuming StatusPage is properly defined in 'status_page' module
from status_page import StatusPage

class DisplayPage(tk.Frame):
    def __init__(self, master, tracker):
        super().__init__(master)
        self.tracker = tracker
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        top_border = tk.Frame(self, bg='DodgerBlue3', height=90)
        top_border.pack(fill="x", side="top")

        tk.Label(self, text="Display Page", font=('Helvetica', 24, 'bold')).pack(pady=20)
        self.bg_image = PhotoImage(file="image__6.png")  # Ensure this path is correct
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.update_button = tk.Button(self, text="Click here to see who should pay!", fg='midnight blue', bg='white',
                                       font=('Bold Condensed', 30, 'bold'), command=self.update_payment)
        self.update_button.pack(pady=10)

        self.display_button = tk.Button(self, text="Budget in detail", fg='midnight blue', bg='white',
                                        font=('Bold Condensed', 30, 'bold'), command=self.display_status)
        self.display_button.pack(pady=10)

        self.why_pay_button = tk.Button(self, text="Why me!", fg='midnight blue', bg='white',
                                        font=('Bold Condensed', 30, 'bold'), command=self.show_why_pay)
        self.why_pay_button.pack(pady=10)

        self.exit_button = tk.Button(self, text="Exit", fg='midnight blue', bg='white',
                                     font=('Bold Condensed', 30, 'bold'), command=self.exit_app)
        self.exit_button.pack(pady=10)

        bottom_border = tk.Frame(self, bg='DodgerBlue3', height=90)
        bottom_border.pack(fill="x", side="bottom")

    def update_payment(self):
        payer = self.tracker.who_pays_next()
        self.tracker.update_payment(payer)
        messagebox.showinfo("Payment Updated", f"{payer} should pay this time.")

    def display_status(self):
        StatusPage(self.tracker)

    def show_why_pay(self):
        debts = self.tracker.calculate_individual_debts()
        # Format the message to display
        message = "\n".join([f"{name} spent a total of: {total_owed}" for name, total_owed in debts])
        messagebox.showinfo("Debts Summary", message)

    def exit_app(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.tracker.close_connection()
            self.master.destroy()
