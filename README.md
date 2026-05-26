# Inventory Management System (Tkinter)

An inventory management app built with Python, Tkinter, and SQLite. It supports Admin and Employee roles, includes billing, and provides a modern single-window dashboard experience.

## Features
- Role-based access: Admin vs Employee
- Dashboard overview for Admin
- Employee, Supplier, Category, Product management
- Sales history and Billing
- SQLite database (local file)

## Screens
- Dashboard (Admin)
- Employee Management (Admin)
- Supplier Management (Admin)
- Category Management (Admin)
- Product Management (Admin)
- Sales History (Admin)
- Billing (Employee)

## Getting Started

### Requirements
- Python 3.10+
- Tkinter (bundled with most Python installs)
- Pillow

### Install Dependencies
```bash
pip install pillow
```

### Run
```bash
python login.py
```

The login screen authenticates against the `employee` table. Users with `utype=Admin` open the Dashboard. Users with `utype=Employee` open Billing.

#### For first time use
Admin login:  
E-mail: admin@ims.com  
Password: admin    
   
Employee login:  
E-mail: emp@ims.com  
Password: emp  
  
You can change the intial e-mall and password at Employee section.


## Project Structure
- login.py - login and role routing
- dashboard.py - main app shell and navigation
- billing.py - billing screen for employees
- employee.py, supplier.py, category.py, product.py, sales.py - management views
- create_db.py - database schema

## Database
SQLite file: `ims.db`

## Credits
Originally developed by Amit Kumar Datta.

## License
[MIT License](LICENSE)
