import sqlite3

def connect_db():
    conn = sqlite3.connect('bank.db')
    conn.execute('''PRAGMA foreign_keys=ON''')
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, 
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone TEXT NOT NULL
    )
    ''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    account_number TEXT UNIQUE NOT NULL,
    balance INTEGER NOT NULL DEFAULT 0 CHECK(balance >= 0),
    account_status TEXT NOT NULL DEFAULT 'Active'
    CHECK(account_status IN ('Active', 'Closed')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    account_number TEXT NOT NULL,
    transaction_type TEXT NOT NULL
    CHECK(transaction_type IN ('Deposit', 'Withdraw', 'Transfer In', 'Transfer Out')),
    amount INTEGER NOT NULL DEFAULT 0 CHECK(amount > 0),
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS admins(id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL)''')

    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_transactions_customer
    ON transactions(customer_id)
    ''')

    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_transactions_account
    ON transactions(account_number)
    ''')

    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_transactions_timestamp
    ON transactions(timestamp)
    ''')
    conn.commit()
    conn.close()