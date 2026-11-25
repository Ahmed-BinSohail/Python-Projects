# Banking Management System

A Python-based Banking Management System with a graphical user interface (GUI), customer and administrator authentication, account management, and transaction processing.

## Features

### Customer Features

- Customer registration and login
- View and update profile
- Create and manage bank accounts
- Check account balances
- Deposit and withdraw money
- Transfer money between accounts
- View transaction history
- Generate account statements
- Change and reset passwords
- Close bank accounts

### Administrator Features

- Admin authentication
- View, search, update, and delete customers
- View and search bank accounts
- Close and reactivate bank accounts
- View banking statistics
- View and search transactions
- Filter transactions by type and date
- Generate transaction summaries
- Create new administrator accounts

## Technologies Used

- **Python** – Application logic
- **Tkinter** – Graphical User Interface
- **SQLite** – Database management
- **Argon2** – Password hashing
- **PyCharm** – Development environment

## Project Structure

```text
Banking Management System/
│
├── main.py
├── gui.py
├── bank.py
├── account.py
├── database.py
├── requirements.txt
├── README.md
│
└── screenshots/
    ├── login.png
    ├── customer_dashboard.png
    └── admin_dashboard.png
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ahmed-BinSohail/Python-Projects
```

### 2. Navigate to the Project Folder

```bash
cd Banking-Management-System
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

For the graphical interface:

```bash
python gui.py
```

For the command-line interface:

```bash
python main.py
```

## Screenshots

### Login Screen
![Login screen.png](../Screenshots/Login%20screen.png)



### Customer Dashboard

![Customer Dashboard.png](../Screenshots/Customer%20Dashboard.png)

### Admin Dashboard

![Admin Dashboard.png](../Screenshots/Admin%20Dashboard.png)

## Security

- Passwords are stored using Argon2 hashing.
- SQLite parameterized queries are used for database operations.
- Customer and administrator authentication are supported.

## Author

**Ahmed Sohail**

Computer Science & Information Technology Student
NED University of Engineering & Technology

---

*Developed as a Python programming project.*
