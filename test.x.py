from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import re  # Regular expression module for validating the user ID

# Function to add an expense
def add_expense(user_id):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"Current Date and Time: {current_time}")
    
    category = input("Enter category: ")
    
    # Asking the user to choose between Credit or Debit
    transaction_type = input("Choose transaction type (1) Credit or (2) Debit: ")
    
    if transaction_type == '1':
        amount = float(input("Enter credit amount: "))
    elif transaction_type == '2':
        amount = -float(input("Enter debit amount: "))
    else:
        print("Invalid choice. Please choose 1 for Credit or 2 for Debit.")
        return

    # Save the expense in a CSV file
    with open(f'{user_id}_expenses.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, category, amount])

    print("Expense added!")


# Function to view all expenses in a table format
def view_expenses(user_id):
    try:
        with open(f'{user_id}_expenses.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

            if rows:
                # Print the table header
                print(f"{'Date':<15} {'Time':<15} {'Category':<20} {'Amount':<10} {'Transaction Type'}")
                print("-" * 70)

                # Print each row in a tabular format
                for row in rows:
                    date_time, category, amount = row
                    date, time = date_time.split(" ")  # Separate date and time
                    transaction_type = "Credit" if float(amount) > 0 else "Debit"
                    # Format the amount with a dollar sign and 2 decimal places
                    print(f"{date:<15} {time:<15} {category:<20} ${float(amount):<10.2f} {transaction_type}")

            else:
                print("No expenses recorded yet.")
    except FileNotFoundError:
        print("No expenses recorded yet.")


# Function to generate a report that shows a breakdown of credits and debits by category
def generate_report(user_id):
    debited_amount = 0.0
    credited_amount = 0.0
    credit_categories = {}
    debit_categories = {}

    try:
        with open(f'{user_id}_expenses.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                date_time, category, amount = row
                if float(amount) > 0:  # Credit
                    credited_amount += float(amount)
                    if category not in credit_categories:
                        credit_categories[category] = 0.0
                    credit_categories[category] += float(amount)
                elif float(amount) < 0:  # Debit
                    debited_amount += abs(float(amount))  # Keep debit as positive value
                    if category not in debit_categories:
                        debit_categories[category] = 0.0
                    debit_categories[category] += abs(float(amount))

        print("\nExpense Report Summary:")

        # Print credit categories and totals
        print("\nCredit Breakdown:")
        print(f"{'Category':<20} {'Amount':<10}")
        print("-" * 30)
        for category, amount in credit_categories.items():
            print(f"{category:<20} ${amount:<10.2f}")
        print("-" * 30)
        print(f"{'Total Credit':<20} ${credited_amount:<10.2f}")

        # Print debit categories and totals
        print("\nDebit Breakdown:")
        print(f"{'Category':<20} {'Amount':<10}")
        print("-" * 30)
        for category, amount in debit_categories.items():
            print(f"{category:<20} ${amount:<10.2f}")
        print("-" * 30)
        print(f"{'Total Debit':<20} ${debited_amount:<10.2f}")

        # Profit or loss
        if credited_amount > debited_amount:
            profit = credited_amount - debited_amount
            print(f"\nYou are in Profit: ${profit:.2f}")
        elif debited_amount > credited_amount:
            loss = debited_amount - credited_amount
            print(f"\nYou are in Loss: ${loss:.2f}")
        else:
            print("\nYou are neither in profit nor in loss.")

    except FileNotFoundError:
        print("No expenses recorded yet.")
        return

    # Return the debited and credited amounts for exporting if needed
    return debited_amount, credited_amount, credit_categories, debit_categories


# Function to export the report (both CSV and PDF formats)
def export_report(user_id, debited_amount, credited_amount, credit_categories, debit_categories):
    export_format = input("Export report as (1) CSV or (2) PDF: ")

    if export_format == '1':
        # Export to CSV with table format and proper cell size
        with open(f'{user_id}_expenses_report.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Credit Breakdown Table
            writer.writerow(['Credit Breakdown'])
            writer.writerow(['Category', 'Amount'])
            writer.writerow(['-' * 20, '-' * 10])  # separator
            for category, amount in credit_categories.items():
                writer.writerow([category.ljust(30), f"${amount:<10.2f}"])
            writer.writerow(['-' * 30, '-' * 10])  # separator
            writer.writerow(['Total Credit'.ljust(30), f"${credited_amount:<10.2f}"])

            # Add some space between sections
            writer.writerow([])
            writer.writerow([])

            # Debit Breakdown Table
            writer.writerow(['Debit Breakdown'])
            writer.writerow(['Category', 'Amount'])
            writer.writerow(['-' * 20, '-' * 10])  # separator
            for category, amount in debit_categories.items():
                writer.writerow([category.ljust(30), f"${amount:<10.2f}"])
            writer.writerow(['-' * 30, '-' * 10])  # separator
            writer.writerow(['Total Debit'.ljust(30), f"${debited_amount:<10.2f}"])

            # Profit or Loss
            if credited_amount > debited_amount:
                profit = credited_amount - debited_amount
                writer.writerow(['Profit'.ljust(30), f"${profit:.2f}"])
            elif debited_amount > credited_amount:
                loss = debited_amount - credited_amount
                writer.writerow(['Loss'.ljust(30), f"${loss:.2f}"])
            else:
                writer.writerow(['No Profit/Loss'.ljust(30), ''])

        print("Report exported as CSV.")

    elif export_format == '2':
        # Export to PDF with table format and proper cell size
        pdf_filename = f'{user_id}_expenses_report.pdf'
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.setFont("Helvetica", 10)

        y = 730
        c.drawString(100, y, "Expense Report Summary")
        y -= 20

        # Credit Breakdown Table
        c.drawString(100, y, "Credit Breakdown:")
        y -= 20
        c.drawString(100, y, f"{'Category':<30} {'Amount':<10}")
        y -= 20
        for category, amount in credit_categories.items():
            c.drawString(100, y, f"{category:<30} ${amount:<10.2f}")
            y -= 20
        c.drawString(100, y, f"Total Credit   ${credited_amount:<10.2f}")
        y -= 40  # Add space after Credit Breakdown

        # Debit Breakdown Table
        c.drawString(100, y, "Debit Breakdown:")
        y -= 20
        c.drawString(100, y, f"{'Category':<30} {'Amount':<10}")
        y -= 20
        for category, amount in debit_categories.items():
            c.drawString(100, y, f"{category:<30} ${amount:<10.2f}")
            y -= 20
        c.drawString(100, y, f"Total Debit    ${debited_amount:<10.2f}")
        y -= 40  # Add space after Debit Breakdown

        # Profit or Loss
        if credited_amount > debited_amount:
            profit = credited_amount - debited_amount
            c.drawString(100, y, f"You are in Profit: ${profit:.2f}")
        elif debited_amount > credited_amount:
            loss = debited_amount - credited_amount
            c.drawString(100, y, f"You are in Loss: ${loss:.2f}")
        else:
            c.drawString(100, y, "You are neither in profit nor in loss.")
        y -= 20

        c.save()
        print("Report exported as PDF.")

    else:
        print("Invalid format selected.")
        # Function to delete an expense by serial number
def delete_expense(user_id):
    try:
        with open(f'{user_id}_expenses.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

            if rows:
                # Display expenses with serial numbers
                print("\nSelect an expense to delete:")
                print(f"{'Serial No.':<12} {'Date':<15} {'Time':<15} {'Category':<20} {'Amount':<10} {'Transaction Type'}")
                print("-" * 70)
                
                for idx, row in enumerate(rows):
                    date_time, category, amount = row
                    date, time = date_time.split(" ")  # Separate date and time
                    transaction_type = "Credit" if float(amount) > 0 else "Debit"
                    # Display each row with serial number
                    print(f"{idx + 1:<12} {date:<15} {time:<15} {category:<20} ${float(amount):<10.2f} {transaction_type}")

                # Ask the user to choose a serial number to delete
                serial_no = int(input("\nEnter the serial number of the expense to delete: ")) - 1

                if 0 <= serial_no < len(rows):
                    print(f"Deleting expense: {', '.join(rows[serial_no])}")
                    del rows[serial_no]  # Delete the selected row

                    # Write the updated rows back to the file
                    with open(f'{user_id}_expenses.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)
                    print("Expense deleted!")
                else:
                    print("Invalid serial number. Please try again.")
            else:
                print("No expenses recorded yet.")
    except FileNotFoundError:
        print("No expenses recorded yet.")
        
        # Function to modify an expense
def modify_expense(user_id):
    try:
        with open(f'{user_id}_expenses.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

            if rows:
                # Display all expenses with serial numbers
                print("\nSelect an expense to modify:")
                print(f"{'Serial No.':<12} {'Date':<15} {'Time':<15} {'Category':<20} {'Amount':<10} {'Transaction Type'}")
                print("-" * 70)
                
                for idx, row in enumerate(rows):
                    date_time, category, amount = row
                    date, time = date_time.split(" ")  # Separate date and time
                    transaction_type = "Credit" if float(amount) > 0 else "Debit"
                    # Display each row with serial number
                    print(f"{idx + 1:<12} {date:<15} {time:<15} {category:<20} ${float(amount):<10.2f} {transaction_type}")

                # Ask the user to choose an expense by serial number
                serial_no = int(input("\nEnter the serial number of the expense to modify: ")) - 1

                if 0 <= serial_no < len(rows):
                    # Display the selected expense
                    print(f"\nSelected expense: {', '.join(rows[serial_no])}")
                    # Prompt user for modification choice
                    print("\nWhat do you want to modify?")
                    print("1. Category")
                    print("2. Amount")
                    print("3. Transaction Type (Credit/Debit)")
                    choice = input("Enter the number of the option to modify: ")

                    if choice == '1':
                        new_category = input("Enter new category: ")
                        rows[serial_no][1] = new_category  # Update the category
                        print(f"Category updated to '{new_category}'.")

                    elif choice == '2':
                        new_amount = float(input("Enter new amount: "))
                        # Update amount and adjust transaction type (Credit/Debit)
                        rows[serial_no][2] = str(new_amount)
                        print(f"Amount updated to ${new_amount:.2f}.")
                        
                    elif choice == '3':
                        transaction_type = input("Choose new transaction type (1) Credit or (2) Debit: ")
                        if transaction_type == '1':
                            rows[serial_no][2] = str(abs(float(rows[serial_no][2])))  # Make the amount positive (Credit)
                            print("Transaction type updated to Credit.")
                        elif transaction_type == '2':
                            rows[serial_no][2] = str(-abs(float(rows[serial_no][2])))  # Make the amount negative (Debit)
                            print("Transaction type updated to Debit.")
                        else:
                            print("Invalid choice. No changes made.")
                            return
                    else:
                        print("Invalid option. No changes made.")
                        return

                    # Write the updated rows back to the CSV file
                    with open(f'{user_id}_expenses.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)
                    print("Expense updated successfully!")

                else:
                    print("Invalid serial number. Please try again.")
            else:
                print("No expenses recorded yet.")
    except FileNotFoundError:
        print("No expenses recorded yet.")
      
        # Function to sort expenses
        def sort_expenses(user_id):
    try:
        # Read the expenses from the CSV file
        with open(f'{user_id}_expenses.csv', 'r') as file:
            reader = csv.reader(file)
            expenses = [row for row in reader]

        if not expenses:
            print("No expenses recorded yet.")
            return

        # Show all expenses
        print("\nList of all expenses:")
        print(f"{'Serial No.':<12} {'Date':<15} {'Time':<15} {'Category':<20} {'Amount':<10} {'Transaction Type'}")
        print("-" * 70)
        for idx, row in enumerate(expenses):
            date_time, category, amount = row
            date, time = date_time.split(" ")  # Separate date and time
            transaction_type = "Credit" if float(amount) > 0 else "Debit"
            # Display each row with serial number
            print(f"{idx + 1:<12} {date:<15} {time:<15} {category:<20} ${float(amount):<10.2f} {transaction_type}")

        # Ask the user which parameter they want to sort by
        print("\nChoose the parameter to sort by:")
        print("1. Date")
        print("2. Time")
        print("3. Category")
        print("4. Amount")
        print("5. Transaction Type (Credit/Debit)")
        
        sort_choice = input("Enter the number of the parameter to sort by: ")

        if sort_choice == '1':  # Sort by date
            date_input = input("Enter the date (YYYY-MM-DD): ")
            filtered_expenses = [row for row in expenses if row[0].startswith(date_input)]
            display_filtered_expenses(filtered_expenses)
            
        elif sort_choice == '2':  # Sort by time
            time_input = input("Enter the time (HH:MM): ")
            filtered_expenses = [row for row in expenses if row[0].endswith(time_input)]
            display_filtered_expenses(filtered_expenses)
            
        elif sort_choice == '3':  # Sort by category
            category_input = input("Enter the category: ")
            filtered_expenses = [row for row in expenses if row[1].lower() == category_input.lower()]
            display_filtered_expenses(filtered_expenses)
        
        elif sort_choice == '4':  # Sort by amount
            amount_input = float(input("Enter the amount (e.g., 647): "))
            lower_limit = amount_input - 50  # Define the range
            upper_limit = amount_input + 50  # Define the range
            filtered_expenses = [row for row in expenses if lower_limit <= float(row[2]) <= upper_limit]
            display_filtered_expenses(filtered_expenses)

        elif sort_choice == '5':  # Sort by transaction type (Credit/Debit)
            transaction_type_input = input("Choose transaction type: (1) Credit or (2) Debit: ")
            if transaction_type_input == '1':
                date_input = input("Enter the date (YYYY-MM-DD) for Credit transactions: ")
                filtered_expenses = [row for row in expenses if row[2] > '0' and row[0].startswith(date_input)]
                display_filtered_expenses(filtered_expenses)
            elif transaction_type_input == '2':
                date_input = input("Enter the date (YYYY-MM-DD) for Debit transactions: ")
                filtered_expenses = [row for row in expenses if row[2] < '0' and row[0].startswith(date_input)]
                display_filtered_expenses(filtered_expenses)
            else:
                print("Invalid choice. Please try again.")

        else:
            print("Invalid choice. Please try again.")

    except FileNotFoundError:
        print("No expenses recorded yet.")
        
def display_filtered_expenses(filtered_expenses):
    if filtered_expenses:
        print(f"\nFiltered expenses:")
        print(f"{'Serial No.':<12} {'Date':<15} {'Time':<15} {'Category':<20} {'Amount':<10} {'Transaction Type'}")
        print("-" * 70)
        for idx, row in enumerate(filtered_expenses):
            date_time, category, amount = row
            date, time = date_time.split(" ")  # Separate date and time
            transaction_type = "Credit" if float(amount) > 0 else "Debit"
            # Display filtered results
            print(f"{idx + 1:<12} {date:<15} {time:<15} {category:<20} ${float(amount):<10.2f} {transaction_type}")
    else:
        print("No expenses found for the specified filter.")


# Function to create or verify user ID and password
def get_user_id_and_password():
    users = {}
    try:
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                users[row[0]] = row[1]
    except FileNotFoundError:
        pass

    # User ID pattern: At least 3 alphabetic characters followed by at least 4 numeric characters
    user_id_pattern = re.compile(r'^[a-zA-Z]{3,}[0-9]{4,}$')  # At least 3 letters followed by 4 digits
    
    while True:
        user_choice = input("Do you want to (1) Login with existing user ID or (2) Create a new user? (1/2): ")
        
        if user_choice == '1':
            user_id = input("Enter your user ID (format: at least 3 letters followed by at least 4 digits, e.g., John1234): ")
            
            if user_id not in users:
                print("Invalid user ID. Please try again.")
                continue
            
            password = input("Enter your password: ")
            if users[user_id] == password:
                print("Login successful!")
                return user_id
            else:
                print("Incorrect password. Please try again.")
        
        elif user_choice == '2':
            while True:
                user_id = input("Create a new user ID (format: at least 3 letters followed by at least 4 digits, e.g., John1234): ")
                
                if user_id_pattern.match(user_id):
                    if user_id not in users:
                        password = input("Create a new password: ")
                        users[user_id] = password
                        with open('users.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([user_id, password])
                        print(f"New user ID '{user_id}' created successfully!")
                        return user_id
                    else:
                        print("User ID already exists. Please try again.")
                else:
                    print("Invalid user ID format. Ensure it has at least 3 letters and 4 digits.")
        else:
            print("Invalid choice. Please choose 1 for login or 2 to create a new user.")


# Main function with a simple menu
def main():
    # Get user ID and password (login or create new user)
    user_id = get_user_id_and_password()

    while True:
        print("\n1. Add Expense")
        print("2. View All Expenses")
        print("3. Generate Report")
        print("4. Export Report")
        print("5. Delete Expense")
        print("6. Modify Expense")
        print("7. Sort Expenses")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense(user_id)
        elif choice == '2':
            view_expenses(user_id)
        elif choice == '3':
            debited_amount, credited_amount, credit_categories, debit_categories = generate_report(user_id)
        elif choice == '4':
            if 'debited_amount' in locals() and 'credited_amount' in locals():
                export_report(user_id, debited_amount, credited_amount, credit_categories, debit_categories)
            else:
                print("Please generate a report first before exporting.")
        elif choice == '5':
            delete_expense(user_id)
        elif choice == '6':
            modify_expense(user_id)
        elif choice == '7':
            sort_by = input("Sort by 'amount' or 'date': ")
            if sort_by == 'date':
                start_date = input("Enter start date (YYYY-MM-DD HH:MM) or leave blank: ") or None
                end_date = input("Enter end date (YYYY-MM-DD HH:MM) or leave blank: ") or None
                sort_expenses(user_id, sort_by, start_date, end_date)
            else:
                sort_expenses(user_id, sort_by)
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


# Run the main function
if _name_ == "_main_":
    main()
