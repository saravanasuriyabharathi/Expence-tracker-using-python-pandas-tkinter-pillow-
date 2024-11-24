import pandas as pd
from tkinter import Tk, Label, Entry, Button, Text, filedialog, messagebox
from tkinter.ttk import Treeview, Style
from PIL import Image, ImageTk

# Create the main application class
class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Add background image
        self.bg_image = Image.open("backround.jpg")  # Replace with your background image path
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Expense DataFrame
        self.data = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

        # Styling
        style = Style()
        style.configure("Treeview", background="#f3f3f3", foreground="black", rowheight=25, fieldbackground="#f3f3f3")
        style.map("Treeview", background=[("selected", "#4CAF50")])

        # Title
        self.title_label = Label(root, text="Expense Tracker", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="black")
        self.title_label.pack(pady=10)

        # Input Fields
        self.add_inputs()

        # Expense Table
        self.add_table()

        # Save Button
        self.save_button = Button(root, text="Save to CSV", font=("Arial", 12), command=self.save_to_csv, bg="#4CAF50", fg="white")
        self.save_button.pack(pady=10)

    def add_inputs(self):
        Label(self.root, text="Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f0f0").place(x=50, y=80)
        self.date_entry = Entry(self.root, font=("Arial", 12))
        self.date_entry.place(x=200, y=80, width=200)

        Label(self.root, text="Category:", font=("Arial", 12), bg="#f0f0f0").place(x=50, y=120)
        self.category_entry = Entry(self.root, font=("Arial", 12))
        self.category_entry.place(x=200, y=120, width=200)

        Label(self.root, text="Amount:", font=("Arial", 12), bg="#f0f0f0").place(x=50, y=160)
        self.amount_entry = Entry(self.root, font=("Arial", 12))
        self.amount_entry.place(x=200, y=160, width=200)

        Label(self.root, text="Description:", font=("Arial", 12), bg="#f0f0f0").place(x=50, y=200)
        self.description_entry = Entry(self.root, font=("Arial", 12))
        self.description_entry.place(x=200, y=200, width=200)

        # Add Expense Button
        self.add_button = Button(self.root, text="Add Expense", font=("Arial", 12), command=self.add_expense, bg="#4CAF50", fg="white")
        self.add_button.place(x=200, y=250)

    def add_table(self):
        self.tree = Treeview(self.root, columns=("Date", "Category", "Amount", "Description"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.column("Date", width=150)
        self.tree.column("Category", width=150)
        self.tree.column("Amount", width=100)
        self.tree.column("Description", width=200)
        self.tree.place(x=50, y=300, width=700, height=250)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        description = self.description_entry.get()

        if not date or not category or not amount or not description:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            amount = float(amount)
            new_expense = {"Date": date, "Category": category, "Amount": amount, "Description": description}
            self.data = pd.concat([self.data, pd.DataFrame([new_expense])], ignore_index=True)

            # Add data to the treeview
            self.tree.insert("", "end", values=(date, category, amount, description))

            # Clear input fields
            self.date_entry.delete(0, "end")
            self.category_entry.delete(0, "end")
            self.amount_entry.delete(0, "end")
            self.description_entry.delete(0, "end")
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")

    def save_to_csv(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            self.data.to_csv(save_path, index=False)
            messagebox.showinfo("Success", f"Data saved to {save_path}!")


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = ExpenseTracker(root)
    root.mainloop()
