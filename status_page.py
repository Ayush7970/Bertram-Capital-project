import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class StatusPage(tk.Toplevel):
    def __init__(self, tracker):
        super().__init__()
        self.tracker = tracker
        self.title("Budget in Detail")
        self.show_members_data()

    def show_members_data(self):
        tree = ttk.Treeview(self)
        tree.pack(fill="both", expand=True)

        # Define columns to match the database structure
        columns = (
        "ID", "Name", "Bob owes", "Jeremy owes", "Alice owes", "Tom owes", "Sarah owes", "Mike owes", "Emma owes")
        tree["columns"] = columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide the first column

        # Set column widths and alignment
        for col in columns:
            tree.column(col, anchor=tk.CENTER, width=80)
            tree.heading(col, text=col)  # Set the headings to match the column names

        # Fetch and insert data
        cursor = self.tracker.conn.cursor()
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)
        cursor.close()
