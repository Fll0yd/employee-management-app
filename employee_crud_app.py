import os
from tkinter import *
from tkinter import messagebox
import mysql.connector
import mysql.connector.pooling


# =========================
# Database Configuration
# =========================
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "employee"),
}

TABLE_NAME = "empDetails"

try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="employee_pool",
        pool_size=5,
        pool_reset_session=True,
        **DB_CONFIG
    )
except mysql.connector.Error as err:
    connection_pool = None
    print(f"Database pool initialization failed: {err}")


# =========================
# Database Helpers
# =========================
def get_connection():
    if connection_pool is None:
        raise mysql.connector.Error("Database connection pool is not available.")
    return connection_pool.get_connection()


def execute_query(query, values=None, fetch_one=False, fetch_all=False):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values or ())
        connection.commit()

        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()
        return None

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error executing query:\n{err}")
        return None

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def ensure_table_exists():
    query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        empId VARCHAR(20) PRIMARY KEY,
        empName VARCHAR(100) NOT NULL,
        empDept VARCHAR(100) NOT NULL
    )
    """
    execute_query(query)


# =========================
# UI Helpers
# =========================
def clear_fields():
    entry_emp_id.delete(0, END)
    entry_emp_name.delete(0, END)
    entry_emp_dept.delete(0, END)


def get_form_data():
    emp_id = entry_emp_id.get().strip()
    emp_name = entry_emp_name.get().strip()
    emp_dept = entry_emp_dept.get().strip()
    return emp_id, emp_name, emp_dept


def populate_listbox():
    listbox_employees.delete(0, END)
    rows = execute_query(
        f"SELECT empId, empName, empDept FROM {TABLE_NAME} ORDER BY empId",
        fetch_all=True
    )

    if not rows:
        return

    for row in rows:
        emp_id, emp_name, emp_dept = row
        listbox_employees.insert(END, f"{emp_id} | {emp_name} | {emp_dept}")


def on_listbox_select(event):
    selection = listbox_employees.curselection()
    if not selection:
        return

    selected_text = listbox_employees.get(selection[0])
    parts = selected_text.split(" | ")

    if len(parts) != 3:
        return

    emp_id, emp_name, emp_dept = parts

    clear_fields()
    entry_emp_id.insert(0, emp_id)
    entry_emp_name.insert(0, emp_name)
    entry_emp_dept.insert(0, emp_dept)


# =========================
# CRUD Actions
# =========================
def insert_data():
    emp_id, emp_name, emp_dept = get_form_data()

    if not emp_id or not emp_name or not emp_dept:
        messagebox.showwarning("Missing Data", "All fields are required.")
        return

    existing = execute_query(
        f"SELECT empId FROM {TABLE_NAME} WHERE empId = %s",
        (emp_id,),
        fetch_one=True
    )

    if existing:
        messagebox.showwarning("Duplicate ID", f"Employee ID '{emp_id}' already exists.")
        return

    execute_query(
        f"INSERT INTO {TABLE_NAME} (empId, empName, empDept) VALUES (%s, %s, %s)",
        (emp_id, emp_name, emp_dept)
    )

    messagebox.showinfo("Insert Status", "Employee added successfully.")
    clear_fields()
    populate_listbox()


def update_data():
    emp_id, emp_name, emp_dept = get_form_data()

    if not emp_id or not emp_name or not emp_dept:
        messagebox.showwarning("Missing Data", "All fields are required.")
        return

    existing = execute_query(
        f"SELECT empId FROM {TABLE_NAME} WHERE empId = %s",
        (emp_id,),
        fetch_one=True
    )

    if not existing:
        messagebox.showwarning("Not Found", f"No employee found with ID '{emp_id}'.")
        return

    execute_query(
        f"UPDATE {TABLE_NAME} SET empName = %s, empDept = %s WHERE empId = %s",
        (emp_name, emp_dept, emp_id)
    )

    messagebox.showinfo("Update Status", "Employee updated successfully.")
    clear_fields()
    populate_listbox()


def delete_data():
    emp_id, _, _ = get_form_data()

    if not emp_id:
        messagebox.showwarning("Missing ID", "Please enter the Employee ID to delete.")
        return

    existing = execute_query(
        f"SELECT empId FROM {TABLE_NAME} WHERE empId = %s",
        (emp_id,),
        fetch_one=True
    )

    if not existing:
        messagebox.showwarning("Not Found", f"No employee found with ID '{emp_id}'.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete employee ID '{emp_id}'?"
    )

    if not confirm:
        return

    execute_query(
        f"DELETE FROM {TABLE_NAME} WHERE empId = %s",
        (emp_id,)
    )

    messagebox.showinfo("Delete Status", "Employee deleted successfully.")
    clear_fields()
    populate_listbox()


def fetch_data():
    emp_id, _, _ = get_form_data()

    if not emp_id:
        messagebox.showwarning("Missing ID", "Please enter an Employee ID to fetch.")
        return

    row = execute_query(
        f"SELECT empId, empName, empDept FROM {TABLE_NAME} WHERE empId = %s",
        (emp_id,),
        fetch_one=True
    )

    if not row:
        messagebox.showinfo("Fetch Status", f"No employee found with ID '{emp_id}'.")
        return

    clear_fields()
    entry_emp_id.insert(0, row[0])
    entry_emp_name.insert(0, row[1])
    entry_emp_dept.insert(0, row[2])


# =========================
# GUI Setup
# =========================
window = Tk()
window.title("Employee Management App")
window.geometry("760x420")
window.resizable(False, False)

title_label = Label(
    window,
    text="Employee Management App",
    font=("Arial", 18, "bold")
)
title_label.place(x=20, y=15)

# Labels
label_emp_id = Label(window, text="Employee ID", font=("Arial", 11))
label_emp_id.place(x=20, y=70)

label_emp_name = Label(window, text="Employee Name", font=("Arial", 11))
label_emp_name.place(x=20, y=110)

label_emp_dept = Label(window, text="Department", font=("Arial", 11))
label_emp_dept.place(x=20, y=150)

# Entries
entry_emp_id = Entry(window, width=30, font=("Arial", 11))
entry_emp_id.place(x=150, y=70)

entry_emp_name = Entry(window, width=30, font=("Arial", 11))
entry_emp_name.place(x=150, y=110)

entry_emp_dept = Entry(window, width=30, font=("Arial", 11))
entry_emp_dept.place(x=150, y=150)

# Buttons
btn_insert = Button(window, text="Insert", width=12, font=("Arial", 10), command=insert_data)
btn_insert.place(x=20, y=210)

btn_update = Button(window, text="Update", width=12, font=("Arial", 10), command=update_data)
btn_update.place(x=130, y=210)

btn_fetch = Button(window, text="Fetch", width=12, font=("Arial", 10), command=fetch_data)
btn_fetch.place(x=240, y=210)

btn_delete = Button(window, text="Delete", width=12, font=("Arial", 10), command=delete_data)
btn_delete.place(x=20, y=260)

btn_reset = Button(window, text="Reset", width=12, font=("Arial", 10), command=clear_fields)
btn_reset.place(x=130, y=260)

btn_refresh = Button(window, text="Refresh List", width=12, font=("Arial", 10), command=populate_listbox)
btn_refresh.place(x=240, y=260)

# Listbox + Scrollbar
listbox_label = Label(window, text="Employees", font=("Arial", 11, "bold"))
listbox_label.place(x=450, y=40)

scrollbar = Scrollbar(window, orient=VERTICAL)
scrollbar.place(x=715, y=70, height=280)

listbox_employees = Listbox(
    window,
    width=38,
    height=16,
    font=("Consolas", 10),
    yscrollcommand=scrollbar.set
)
listbox_employees.place(x=450, y=70)
listbox_employees.bind("<<ListboxSelect>>", on_listbox_select)

scrollbar.config(command=listbox_employees.yview)

# Initialize
ensure_table_exists()
populate_listbox()

window.mainloop()
