# Expense Tracker

A simple command-line application for tracking personal expenses. This application allows users to add expenses, view all recorded expenses, and generate a report of total expenses by category.

## Features

- Add Expense: Input date, category, amount, and an optional description.
- View All Expenses: Display all recorded expenses in a readable format.
- Generate Report: Summarize total expenses by category.
- Persistent Storage: Expenses are saved in a CSV file for future reference.

## Requirements

- Python 3.x
- No external libraries required (uses built-in csv module)

## Getting Started

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Run the application using Python:

   python expense_tracker.py

## Usage

Once the application is running, you will see a menu with the following options:

1. Add Expense: Enter details of the expense you want to add.
2. View All Expenses: View all recorded expenses.
3. Generate Report: Get a summary of total expenses by category.
4. Exit: Close the application.

## Example

Expense Tracker Menu:
1. Add Expense
2. View All Expenses
3. Generate Report
4. Exit
Choose an option: 1
Enter date (YYYY-MM-DD): 2023-10-01
Enter category: Food
Enter amount: 15.50
Enter description (optional): Lunch
Expense added!

## File Structure

- expense_tracker.py: The main application file.
- expenses.csv: The file where all expenses are stored.

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is open-source and available under the MIT License.
