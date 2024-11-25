Expense Tracker Application
Overview
The Expense Tracker Application is a Python-based tool designed to help users manage their expenses efficiently. It allows users to add, view, modify, delete, and generate reports of their expenses, categorized as either credit or debit. The application also supports user authentication, enabling multiple users to maintain their individual expense records securely.

Features
User Authentication: Users can create a new account or log in with an existing user ID and password.
Add Expenses: Users can add expenses with categories, amounts, and transaction types (credit or debit).
View Expenses: Users can view all their recorded expenses in a tabular format.
Modify Expenses: Users can modify existing expenses by changing the category, amount, or transaction type.
Delete Expenses: Users can delete specific expenses from their records.
Generate Reports: Users can generate detailed reports that summarize their credits and debits by category.
Export Reports: Users can export their expense reports in CSV or PDF format.
Sort Expenses: Users can sort their expenses by date, category, amount, or transaction type.
Technologies Used
Python
ReportLab (for PDF generation)
CSV (for data storage)
Regular Expressions (for user ID validation)
Installation
Clone the repository:

bash

Verify

Open In Editor
Edit
Copy code
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
Install the required libraries:

bash

Verify

Open In Editor
Edit
Copy code
pip install reportlab
Usage
Run the application:

bash

Verify

Open In Editor
Edit
Copy code
python expense_tracker.py
Follow the on-screen prompts to create a new user or log in with an existing user ID.

Use the menu options to manage your expenses.

User ID Format
User IDs must contain at least 3 alphabetic characters followed by at least 4 numeric characters (e.g., John1234).
File Structure
expense_tracker.py: The main application file containing the core functionalities.
users.csv: A file that stores user credentials (user ID and password).
user_id_expenses.csv: A CSV file created for each user to store their expenses.
Example Commands
Add Expense: Prompts the user to enter the category, amount, and transaction type.
View All Expenses: Displays all recorded expenses in a table format.
Generate Report: Summarizes credits and debits by category.
Export Report: Allows users to save the report in either CSV or PDF format.
Sort Expenses: Enables users to filter expenses based on selected criteria.
Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Thanks to the Python community for their support and resources.
Special thanks to the developers of ReportLab for their excellent library for PDF generation.
