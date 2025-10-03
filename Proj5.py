import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re
import atexit

class DatabaseManager:
    def __init__(self, db_name='customer_data.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_table()

        atexit.register(self.close)

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")

    def _create_table(self):
        if not self.cursor:
            return

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birthday TEXT,
                email TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                contact_method TEXT
            )
        ''')
        self.conn.commit()
        print("Customer table checked/created successfully.")

    def insert_customer(self, data):
        if not self.cursor:
            return False

        try:
            self.cursor.execute('''
                INSERT INTO customers (name, birthday, email, phone, address, contact_method)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', data)
            self.conn.commit()
            print(f"Data successfully inserted for: {data[0]}")
            return True
        except sqlite3.Error as e:
            print(f"Database insertion error: {e}")
            messagebox.showerror("Insertion Error", f"Failed to save data: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


class CustomerFormApp:
    def __init__(self, master, db_manager):
        self.master = master
        master.title("Customer Information Submission")
        master.geometry("500x550")
        master.resizable(False, False)

        self.db = db_manager
        self.fields = {} 

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Inter', 10), foreground='#333333')
        self.style.configure('TButton', font=('Inter', 10, 'bold'), padding=8, background='#4CAF50', foreground='white')
        self.style.map('TButton',
                       background=[('active', '#45a049'), ('pressed', '#3e8e41')])
        self.style.configure('TCombobox', font=('Inter', 10))

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="New Customer Registration", font=('Inter', 14, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=(0, 20), sticky="w"
        )

        form_config = [
            ("Full Name (Required):", 1, "Entry"),
            ("Date of Birth (YYYY-MM-DD):", 2, "Entry"),
            ("Email (Required):", 3, "Entry"),
            ("Phone Number:", 4, "Entry"),
            ("Address:", 5, "Text"), 
            ("Preferred Contact Method:", 6, "Combobox")
        ]

        row_index = 0
        for label_text, r, field_type in form_config:
            row_index = r
            
            ttk.Label(main_frame, text=label_text).grid(
                row=row_index, column=0, sticky="w", pady=5, padx=5
            )

            if field_type == "Entry":
                field = ttk.Entry(main_frame, width=40, font=('Inter', 10))
            elif field_type == "Text":
                field = tk.Text(main_frame, height=4, width=38, font=('Inter', 10))
            elif field_type == "Combobox":
                field = ttk.Combobox(main_frame, width=38, state="readonly", font=('Inter', 10))
                field['values'] = ('Email', 'Phone', 'Mail', 'Any')
                field.current(0) 
                self.preferred_contact = field
            
            field.grid(row=row_index, column=1, sticky="ew", pady=5, padx=5)
            
            if field_type != "Combobox":
                key = label_text.split(" ")[0].lower().strip(':')
                self.fields[key] = field
        
        submit_btn = ttk.Button(main_frame, text="Submit Information", command=self._submit_data)
        submit_btn.grid(row=row_index + 1, column=0, columnspan=2, pady=20, sticky="ew")

        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="#2E86C1")
        self.status_label.grid(row=row_index + 2, column=0, columnspan=2, sticky="ew")

        main_frame.grid_columnconfigure(1, weight=1)

    def _validate_email(self, email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(regex, email)

    def _clear_form(self):
        for key in self.fields:
            field = self.fields[key]
            if isinstance(field, tk.Text):
                field.delete('1.0', tk.END)
            else:
                field.delete(0, tk.END)
        self.preferred_contact.current(0)


    def _submit_data(self):
        
        name = self.fields['full'].get().strip()
        birthday = self.fields['date'].get().strip()
        email = self.fields['email'].get().strip()
        phone = self.fields['phone'].get().strip()
        
        address = self.fields['address'].get('1.0', tk.END).strip()
        contact_method = self.preferred_contact.get().strip()

        if not name or not email:
            messagebox.showerror("Validation Error", "Name and Email are required fields.")
            return

        if not self._validate_email(email):
            messagebox.showerror("Validation Error", "Please enter a valid email address.")
            return

        data_to_save = (name, birthday, email, phone, address, contact_method)

        if self.db.insert_customer(data_to_save):
            messagebox.showinfo("Success", f"Customer '{name}' information saved successfully!")
            self._clear_form()
            self.status_var.set(f"Last submission: {name} saved successfully.")
        else:
            self.status_var.set("Submission failed. Check console for details.")


if __name__ == '__main__':
    db_manager = DatabaseManager()

    root = tk.Tk()

    app = CustomerFormApp(root, db_manager)

    root.mainloop()
