import sqlite3

def view_customer_data():
    """Connects to the database and prints all customer data."""
    try:
        # Connect to the SQLite database file
        conn = sqlite3.connect('customer_data.db')
        # Create a cursor object
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve all data from the customers table
        cursor.execute("SELECT * FROM customers")

        # Fetch all the rows from the query result
        rows = cursor.fetchall()

        # Get the column names from the cursor description
        column_names = [description[0] for description in cursor.description]
        print(" | ".join(column_names))
        print("-" * (sum(len(name) for name in column_names) + len(column_names) * 3))

        # Print the data
        if not rows:
            print("No data found in the 'customers' table.")
        else:
            for row in rows:
                print(" | ".join(str(item) for item in row))

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    view_customer_data()