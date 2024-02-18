# Project: Bertram Capital Lounge App
# Creator: Ayush Bhardwaj
# Email: ayush975600@gmail.com


import tkinter as tk
from tkinter import PhotoImage
import sqlite3
from welcome import DrinkInputPage


class CoffeePaymentTracker:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.coffee_prices = self.extract_coffee_prices()
        self.coworkers = self.extract_coworker_preferences()

    def extract_coffee_prices(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT Drinks, prices FROM coffee_shop')
        rows = cursor.fetchall()
        return {drink: price for drink, price in rows}

    def extract_coworker_preferences(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT Name FROM members')
        rows = cursor.fetchall()
        return {name[0]: {'drink': None, 'owes': {}} for name in rows}

    def input_drink_preferences(self):
        for name in self.coworkers.keys():
            drink = input(f"Enter {name}'s drink choice: ").upper()
            if drink in self.coffee_prices:
                self.coworkers[name]['drink'] = drink
            else:
                print(f"Invalid drink choice. Available options: {list(self.coffee_prices.keys())}")
                return False
        return True

    def calculate_total_cost(self):
        total_cost = sum(self.coffee_prices[self.coworkers[name]['drink']] for name in self.coworkers if self.coworkers[name]['drink'])
        return total_cost

    def update_payment(self, payer):
        if payer in self.coworkers:
            total_cost = self.calculate_total_cost()
            self.update_database(payer, total_cost)
        else:
            print(f"{payer} is not a recognized coworker.")

    def update_database(self, payer, total_cost):
        cursor = self.conn.cursor()
        for coworker in self.coworkers.keys():
            if coworker != payer:
                individual_cost = self.coffee_prices[self.coworkers[coworker]['drink']]
                cursor.execute(f"UPDATE members SET `{coworker} owes` = `{coworker} owes` + ? WHERE Name = ?", (individual_cost, payer))
        self.conn.commit()



    def display_status(self):
        for name, details in self.coworkers.items():
            print(f"{name} owes: {details['owes']}")
        next_payer = self.who_pays_next()
        print(f"Next to pay: {next_payer}")

    def who_pays_next(self):

        cursor = self.conn.cursor()
        cursor.execute("SELECT Name, (`Bob owes` + `Jeremy owes` + `Alice owes` + `Tom owes` + `Sarah owes` + `Mike owes` + `Emma owes`) AS Total FROM members ORDER BY Total ASC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else "No data"

    def get_budget_details(self):
        # Fetch budget details
        details = {}
        cursor = self.conn.cursor()
        cursor.execute('SELECT Name, (`Bob owes` + `Jeremy owes` + `Alice owes` + `Tom owes` + `Sarah owes` + `Mike owes` + `Emma owes`) AS Total FROM members')
        for row in cursor.fetchall():
            details[row[0]] = row[1]
        cursor.close()
        return details

    def calculate_debts(self):
        cursor = self.conn.cursor()
        # Adjust the SQL query
        cursor.execute("SELECT * from members;")
        results = cursor.fetchall()

        cursor.close()
        return results

    def calculate_individual_debts(self):
        cursor = self.conn.cursor()
        # Correct the SQL query by removing single quotes and adding proper SQL concatenation
        query = """
        SELECT Name, 
               (IFNULL(`Bob owes`, 0) + IFNULL(`Jeremy owes`, 0) + IFNULL(`Alice owes`, 0) + 
                IFNULL(`Tom owes`, 0) + IFNULL(`Sarah owes`, 0) + IFNULL(`Mike owes`, 0) + 
                IFNULL(`Emma owes`, 0)) AS Total_Owed 
        FROM members;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def close_connection(self):
        self.conn.close()


class MainApp(tk.Frame):
    def __init__(self, master, tracker):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.tracker = tracker
        self.load_background_image()
        self.create_widgets()
        self.label = tk.Label(self, text="Welcome to Bertram Capital Lounge!", fg='midnight blue', bg='white',
                              font=('Bold Condensed', 50, 'bold'))
        self.label.pack(pady=20)

    def create_widgets(self):

        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)


        top_border = tk.Frame(self, bg='DodgerBlue3', height=90)
        top_border.pack(fill="x", side="top")

        tk.Button(self, text="Order Now!", command=self.open_drink_input_page,
                  bg='white', fg='midnight blue', font=('Bold Condensed', 40, 'bold')).pack(pady=20, padx=10)

        bottom_border = tk.Frame(self, bg='DodgerBlue3', height=90)
        bottom_border.pack(fill="x", side="bottom")



    def open_drink_input_page(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        DrinkInputPage(self.master, self.tracker)

    def load_background_image(self):
        self.background_image = PhotoImage(file="image__6.png")

if __name__ == "__main__":
    db_path = "BertmanLab.db"
    root = tk.Tk()
    root.title("Coffee Payment Tracker")
    root.geometry("800x600")
    tracker = CoffeePaymentTracker(db_path)
    app = MainApp(root, tracker)
    root.mainloop()
