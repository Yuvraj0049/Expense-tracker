import csv


# Function to add an expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    amount = input("Enter amount: ")
    description = input("Enter description (optional): ")

    # Save the expense in a CSV file
    with open('expenses.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    print("Expense added!")


# Function to view all expenses
def view_expenses():
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(", ".join(row))
    except FileNotFoundError:
        print("No expenses recorded yet.")


# Function to generate a simple report
def generate_report():
    expenses = {}
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[1]
                amount = float(row[2])
                if category in expenses:
                    expenses[category] += amount
                else:
                    expenses[category] = amount
    except FileNotFoundError:
        print("No expenses recorded yet.")
        return

    print("\nExpense Report:")
    for category, total in expenses.items():
        print(f"{category}: ${total:.2f}")


# Main function with a simple menu
def main():
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Generate Report")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


# Run the main function
if __name__ == "__main__":
    main()
