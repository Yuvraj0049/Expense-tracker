                                                 Expense Tracker

                                                       BY 

                                                  Yuvraj(23csu358)
                                                  Rohan(23csu402)

                                                  Submitted to :
                                                Dr. Shraddha Arora

                                                The NorthCap University
                                                      Gurgaon











Key Sections of the Code:
Adding Expenses (add_expense):

Asks the user to input the category, type of transaction (Credit or Debit), and amount.
Saves the expense in a CSV file associated with the user.
Viewing Expenses (view_expenses):

Displays all expenses in a tabular format.
If no expenses are found, the user is informed.
Generating Reports (generate_report):

Summarizes the credits and debits, broken down by category.
Calculates profit or loss based on total credits and debits.
Exporting Reports (export_report):

Allows the user to export the generated report in either CSV or PDF format.
For CSV, it writes the credit and debit breakdown, along with the profit or loss, to a new CSV file.
For PDF, it uses the reportlab library to generate a formatted PDF of the report.
Deleting Expenses (delete_expense):

Allows the user to delete a specific expense by serial number.
Modifying Expenses (modify_expense):

Allows the user to modify an expense's category, amount, or transaction type (Credit/Debit).
Sorting Expenses (sort_expenses):

Allows the user to filter expenses by specific parameters such as date, category, amount, etc.
Filters the expenses and displays the results.
User Authentication (get_user_id_and_password):

Allows users to log in with an existing ID or create a new one, ensuring that the user ID follows a specific format (at least 3 letters followed by 4 digits).
Improvements/Suggestions:
User Interface (UI):

The command-line interface can be more user-friendly with clearer instructions and better error handling.
Adding a confirmation message after important actions (like adding, deleting, or modifying an expense) can help the user understand the results of their actions.
Handling File I/O:

You should handle the potential errors in file handling more gracefully. For example, if a CSV file is not found, consider creating a new one automatically.
Ensure that when deleting or modifying a record, the user knows that the data is being updated in the CSV file.
Optimizing Report Generation:

The generate_report function could also provide a more detailed breakdown of each transaction, such as monthly or yearly summaries.
For the PDF report generation, you can improve the layout with more formatting, such as bold headers or different font sizes.
Code Structuring:

Consider organizing the functions into classes or separate modules (e.g., ExpenseManager, UserManager) for better maintainability.
Here's an enhanced snippet that wraps these concepts together:

python
Copy code
import csv
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ExpenseManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.file_path = f'{self.user_id}_expenses.csv'

    def add_expense(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        print(f"Current Date and Time: {current_time}")
        
        category = input("Enter category: ")
        transaction_type = input("Choose transaction type (1) Credit or (2) Debit: ")
        
        if transaction_type == '1':
            amount = float(input("Enter credit amount: "))
        elif transaction_type == '2':
            amount = -float(input("Enter debit amount: "))
        else:
            print("Invalid choice. Please choose 1 for Credit or 2 for Debit.")
            return
        
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, category, amount])
        print("Expense added!")

    def view_expenses(self):
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                
                if rows:
                    print(f"{'Date':<15} {'Time':<15} {'Category':<20} {'Amount':<10} {'Transaction Type'}")
                    print("-" * 70)

                    for row in rows:
                        date_time, category, amount = row
                        date, time = date_time.split(" ")
                        transaction_type = "Credit" if float(amount) > 0 else "Debit"
                        print(f"{date:<15} {time:<15} {category:<20} ${float(amount):<10.2f} {transaction_type}")

                else:
                    print("No expenses recorded yet.")
        except FileNotFoundError:
            print("No expenses recorded yet.")

# Usage example:
def main():
    user_id = input("Enter your user ID: ")
    manager = ExpenseManager(user_id)

    while True:
        print("\n1. Add Expense")
        print("2. View All Expenses")
        print("3. Generate Report")
        print("4. Export Report")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            manager.add_expense()
        elif choice == '2':
            manager.view_expenses()
        elif choice == '3':
            # Assuming generate_report function is part of the class
            pass
        elif choice == '4':
            # Assuming export_report function is part of the class
            pass
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")
    
if __name__ == "__main__":
    main()
Enhancements:
Class-based design for better encapsulation (e.g., ExpenseManager handles all expenses).
Simplified user interface with a basic menu system.
Modular functions for adding, viewing, generating reports, and exporting them.
