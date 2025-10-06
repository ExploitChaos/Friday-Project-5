# Friday-Project-5

Customer Data Application
This repository contains a simple Python application for collecting and viewing customer information. The application consists of a graphical user interface (GUI) for data entry, a script for viewing the stored data, and an SQLite database file to store the information.

Files
proj5.py
This is the main application file. When run, it launches a GUI that allows customers to enter their personal information. Upon submission, the data is saved directly into the customer_data.db file.

viewdb.py
This utility script is used to view the data stored in the database. It connects to customer_data.db, retrieves all the customer records, and prints them in a formatted, readable table in the console.

customer_data.db
This is the SQLite database file. It acts as the persistent storage for all the customer data entered through the proj5.py application.

How to Use
Enter Customer Data: To open the GUI and begin entering customer information, run proj5.py from your terminal:

Bash

python proj5.py
View Stored Data: To see the data that has been saved to the database, run the viewdb.py script:

Bash

python viewdb.py
This will display a table of all the customer records in your terminal.

Technical Details
Database: The application uses SQLite for data storage, which is a lightweight, serverless database engine. The data is stored in the customer_data.db file within the repository.

GUI: The GUI is built using Python's built-in libraries.

Known Issues: There are no known issues or bugs with the current version of the code.