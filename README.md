# Employee Management App

## Overview
A desktop application for managing employee records using a MySQL backend.  
Built with Python and Tkinter to demonstrate full CRUD operations, database integration, and connection pooling.

## Features
- Add new employee records
- Fetch employee details by ID
- Update existing employee data
- Delete employee records
- Real-time list view of employees
- MySQL connection pooling for efficient database access
- Automatic table creation on startup

## Tech Stack
- **Python**
- **Tkinter (GUI)**
- **MySQL (mysql-connector)**

## Setup

### 1. Create Database
```sql
CREATE DATABASE employee;
```

2. Set Environment Variables

Windows (PowerShell):
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="employee"

Linux / Mac:
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=employee

3. Install Dependencies
pip install mysql-connector-python

4. Run the Application
python employee_crud_app.py

The application will automatically create the required table if it does not exist.


```md
## Project Purpose
This project was built to practice:
```
Database-backed application design
CRUD workflows
GUI development with Tkinter
Efficient database connection handling using pooling

```md
## Future Improvements
```
Input validation and form constraints
Search/filter functionality
Pagination for large datasets
Migration to web-based UI (Flask / FastAPI)
Authentication and user roles


Author

Kenneth Lloyd Boller
