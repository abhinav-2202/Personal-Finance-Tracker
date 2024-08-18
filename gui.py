import io
import sys
import re
from tkinter import *
from tkinter.ttk import Combobox
from main import CSV, plot_transactions
from tkinter import messagebox
from datetime import datetime

class PersonalFinanceTracker:

    def __init__(self, root):
        self.window = root
        self.window.geometry("1000x700")
        self.window.title("Personal Finance Tracker")

        icon = PhotoImage(file='logo.png')
        self.window.iconphoto(True, icon)
        self.window.config(background="#1d1f1d")

        heading = Label(self.window,
                    text="💵💵 Welcome to Personal Finance Tracker 💵💵",
                    font=('Fixedsys', 30),
                    fg="white",
                    bg="#1d1f1d",
                    padx=20,
                    pady=20
                    )
        heading.grid(row=0, column=0, columnspan=2, pady=20)

        #----------ADD A TRANSACTION----------
        subhead_1 = Label(self.window,
                          text="💸💸 Add a transaction 💸💸",
                          font=('Fixedsys', 18),
                          fg="#f7f383",
                          bg="#1d1f1d"
                          )
        subhead_1.grid(row=1, column=0, sticky='w', padx=20)

        # Container frame for labels and entry boxes
        self.form_frame = Frame(self.window, bg="#1d1f1d")
        self.form_frame.grid(row=2, column=0, padx=20, pady=10, sticky='nw')

        # Date Label and Entry box
        label1 = Label(self.form_frame, text="Date (dd-mm-yyyy):", font=('Fixedsys', 14), fg="white", bg="#1d1f1d")
        label1.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.entry1 = Entry(self.form_frame, font=('Fixedsys', 14))
        self.entry1.grid(row=0, column=1, padx=5, pady=5)

        # Amount Label and Entry box
        label2 = Label(self.form_frame, text="Amount:", font=('Fixedsys', 14), fg="white", bg="#1d1f1d")
        label2.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.entry2 = Entry(self.form_frame, font=('Fixedsys', 14))
        self.entry2.grid(row=1, column=1, padx=5, pady=5)

        # Category Label and Combobox
        label3 = Label(self.form_frame, text="Category:", font=('Fixedsys', 14), fg="white", bg="#1d1f1d")
        label3.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.category = Combobox(self.form_frame, font=('Fixedsys', 14), values=["Income", "Expense"])
        self.category.grid(row=2, column=1, padx=5, pady=5)
        self.category.current(1)  # Set default value to "Expense"

        # Description Label and Entry box
        label4 = Label(self.form_frame, text="Description (optional):", font=('Fixedsys', 14), fg="white", bg="#1d1f1d")
        label4.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.entry4 = Entry(self.form_frame, font=('Fixedsys', 14))
        self.entry4.grid(row=3, column=1, padx=5, pady=5)

        # Add Entry Button
        add_button = Button(self.form_frame, text="Add Entry", font=('Fixedsys', 14), bg="#f7f383", fg="#1d1f1d", command=self.add_entry)
        add_button.grid(row=4, column=0, columnspan=2, pady=20)

        #----------VIEW TRANSACTIONS----------
        subhead_2 = Label(self.window,
                          text="📊📊 View transactions 📊📊",
                          font=('Fixedsys', 18),
                          fg="#f7f383",
                          bg="#1d1f1d"
                          )
        subhead_2.grid(row=3, column=0, sticky='w', padx=20)

        # Container frame for view date entries
        self.view_frame = Frame(self.window, bg="#1d1f1d")
        self.view_frame.grid(row=4, column=0, padx=20, pady=10, sticky='nw')

        # Start Date Label and Entry box
        start_date_label = Label(self.view_frame, text="Start Date (dd-mm-yyyy):", font=('Fixedsys', 14), fg="white", bg="#1d1f1d")
        start_date_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.start_date_entry = Entry(self.view_frame, font=('Fixedsys', 14))
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        # End Date Label and Entry box
        end_date_label = Label(self.view_frame, text="End Date (dd-mm-yyyy):", font=('Fixedsys', 14), fg="white", bg="#1d1f1d")
        end_date_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.end_date_entry = Entry(self.view_frame, font=('Fixedsys', 14))
        self.end_date_entry.grid(row=1, column=1, padx=5, pady=5)

        # View Button
        view_button = Button(self.window, text="View", font=('Fixedsys', 14), bg="#f7f383", fg="#1d1f1d", command=self.view_transactions)
        view_button.grid(row=6, column=0, sticky='w', padx=20, pady=10)

       # Text Widget for displaying output, centered in the right half
        self.output_text = Text(self.window, height=25, width=50, font=('Fixedsys', 12), bg="#2d2d2d", fg="white")
        self.output_text.grid(row=1, column=1, rowspan=6, padx=20, pady=20, sticky='n')

        # Clear Output Button
        clear_button = Button(self.window, text="Clear Output", font=('Fixedsys', 14), bg="#f7f383", fg="#1d1f1d", command=self.clear_output)
        clear_button.grid(row=7, column=1, padx=20, pady=10, sticky='n')
    
    def validate_date(self, date_text):
        """Validate the date format dd-mm-yyyy."""
        date_pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$")
        if not date_pattern.match(date_text):
            return False
        return True
    
    def validate_amount(self, amount_text):
        """Validate if the amount is a number."""
        try:
            float(amount_text)
            return True
        except ValueError:
            return False
    
    def validate_category(self, category_text):
        """Validate if the category is either 'Income' or 'Expense'."""
        return category_text in ["Income", "Expense"]

    def add_entry(self):
        # Retrieve values from the entry boxes and combobox
        date_value = self.entry1.get()
        if not self.validate_date(date_value):
            messagebox.showerror("Invalid Date", "Please enter the date in dd-mm-yyyy format.")
            return
        
        amount_value = self.entry2.get()
        if not self.validate_amount(amount_value):
            messagebox.showerror("Invalid Amount", "Please enter a valid number for the amount.")
            return
        
        category_value = self.category.get()
        if not self.validate_category(category_value):
            messagebox.showerror("Invalid Category", "Category must be either 'Income' or 'Expense'.")
            return
        
        description_value = self.entry4.get()

        # Print the values to the console
        self.output_text.insert(END, "-"*40 + "\n")
        self.output_text.insert(END, f"Date: {date_value}\n")
        self.output_text.insert(END, f"Amount: {amount_value}\n")
        self.output_text.insert(END, f"Category: {category_value}\n")
        self.output_text.insert(END, f"Description: {description_value}\n")
        self.output_text.insert(END, f"Entry Added.\n")
        self.output_text.insert(END, "-"*40 + "\n")

        CSV.add_entry(date_value, amount_value, category_value, description_value)

    def view_transactions(self):
        # Retrieve values from the view date entries and checkbox
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not self.validate_date(start_date) or not self.validate_date(end_date):
            messagebox.showerror("Invalid Date", "Please enter the dates in dd-mm-yyyy format.")
            return

        # Print the values to the console
        print("Start Date:", start_date)
        print("End Date:", end_date)

        # Capture the output of get_transactions function
        output_buffer = io.StringIO()
        sys.stdout = output_buffer  # Redirect standard output to the buffer
        
        df = CSV.get_transactions(start_date, end_date)  # Call the function
        
        sys.stdout = sys.__stdout__  # Reset standard output to default
        
        output_text = output_buffer.getvalue()  # Get the printed content
        output_buffer.close()

        # Display the captured output in the Text widget
        self.output_text.insert(END, output_text)
        self.output_text.insert(END, "-"*40 + "\n")

        result = messagebox.askyesno("Plot Graph", "Do you want to plot the graph?")

        if result:
            # If 'Yes' is clicked, plotting the graph
            self.output_text.insert(END, "Plotting graph...\n")
            self.output_text.insert(END, "-"*40 + "\n")
            plot_transactions(df)
        else:
            # If 'No' is clicked, return to the main program
            print("Returning to program...")
    
    def clear_output(self):
        if messagebox.askyesno("Clear Output", "Are you sure you want to clear the output?"):
            self.output_text.delete('1.0', END)


if __name__ == "__main__":
    root = Tk()
    app = PersonalFinanceTracker(root)
    root.mainloop()
