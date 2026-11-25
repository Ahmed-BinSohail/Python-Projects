import random
from dbm import sqlite3

from database import connect_db
from datetime import datetime

def generate_account_number():
    return random.randint(1000000000, 9999999999)


def create_account(customer_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM customers WHERE id = ?",
            (customer_id,)
        )
        customer = cursor.fetchone()

        if not customer:
            return None

        for attempt in range(10):
            account_number = generate_account_number()

            cursor.execute('''
            SELECT id FROM accounts
            WHERE account_number = ?
            ''', (account_number,))

            account = cursor.fetchone()

            if account is None:
                break

        else:
            return None

        cursor.execute('''
        INSERT INTO accounts (customer_id, account_number, balance)
        VALUES (?, ?, ?)
        ''', (customer_id, account_number, 0))

        conn.commit()
        return account_number

    except sqlite3.IntegrityError:
        conn.rollback()
        return None

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()


def view_my_accounts(customer_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        SELECT account_number, balance, account_status
        FROM accounts
        WHERE customer_id = ?
        ''', (customer_id,))

        accounts = cursor.fetchall()

        if not accounts:
            return []

        return accounts

    except sqlite3.Error as e:
        raise

    finally:
        conn.close()




def check_balance(customer_id, account_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        SELECT account_number, balance, account_status
        FROM accounts
        WHERE account_number = ? AND customer_id = ?
        ''', (account_number, customer_id))

        account = cursor.fetchone()

        if not account:
            raise ValueError("Account not found")

        if account[2] != "Active":
            raise ValueError("Account is closed")

        return account

    except sqlite3.Error:
        raise

    finally:
        conn.close()




def deposit_money(customer_id, account_number, amount):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        SELECT id, account_status
        FROM accounts
        WHERE account_number = ? AND customer_id = ?
        ''', (account_number, customer_id))

        account = cursor.fetchone()

        if not account:
            raise ValueError("Account not found")

        if account[1] != "Active":
            raise ValueError("Account is closed")

        if amount <= 0:
            raise ValueError("Enter a valid deposit amount")

        cursor.execute('''
        UPDATE accounts
        SET balance = balance + ?
        WHERE id = ? AND customer_id = ?
        AND account_status = 'Active'
        ''', (amount, account[0], customer_id))

        if cursor.rowcount == 0:
            conn.rollback()
            raise ValueError("Deposit failed. Account unavailable")

        cursor.execute('''
        INSERT INTO transactions
        (customer_id, account_id, account_number, transaction_type, amount)
        VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, account[0], account_number, "Deposit", amount))

        cursor.execute('''
        SELECT balance
        FROM accounts
        WHERE id = ?
        ''', (account[0],))

        new_balance = cursor.fetchone()[0]

        conn.commit()
        return new_balance

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()



def withdraw_money(customer_id, account_number, amount):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        SELECT id, balance, account_status
        FROM accounts
        WHERE account_number = ? AND customer_id = ?
        ''', (account_number, customer_id))

        account = cursor.fetchone()

        if not account:
            raise ValueError("Account not found")

        if account[2] != "Active":
            raise ValueError("Account is closed")

        if amount <= 0:
            raise ValueError("Enter a valid withdrawal amount")

        if account[1] < amount:
            raise ValueError("Insufficient funds")

        cursor.execute('''
        UPDATE accounts
        SET balance = balance - ?
        WHERE id = ? AND customer_id = ?
        AND balance >= ? AND account_status = 'Active'
        ''', (amount, account[0], customer_id, amount))

        if cursor.rowcount == 0:
            conn.rollback()
            raise ValueError("Insufficient funds or account unavailable")

        cursor.execute('''
        INSERT INTO transactions
        (customer_id, account_id, account_number, transaction_type, amount)
        VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, account[0], account_number, "Withdraw", amount))

        cursor.execute('''
        SELECT balance FROM accounts
        WHERE id = ?
        ''', (account[0],))

        new_balance = cursor.fetchone()[0]

        conn.commit()
        return new_balance

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()




def view_transaction_history(customer_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        SELECT id, account_number, transaction_type, amount, timestamp
        FROM transactions
        WHERE customer_id = ?
        ORDER BY timestamp DESC
        ''', (customer_id,))

        transactions = cursor.fetchall()
        return transactions

    except sqlite3.Error:
        raise

    finally:
        conn.close()





def close_account(customer_id, account_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        SELECT id, account_number, balance, account_status
        FROM accounts
        WHERE account_number = ? AND customer_id = ?
        ''', (account_number, customer_id))

        account = cursor.fetchone()

        if not account:
            raise ValueError("Account not found")

        if account[3] == "Closed":
            raise ValueError("Account is already closed")

        if account[3] != "Active":
            raise ValueError("Account is not active")

        if account[2] != 0:
            raise ValueError(
                "Please withdraw your remaining balance before closing this account"
            )

        cursor.execute('''
        UPDATE accounts
        SET account_status = 'Closed'
        WHERE id = ? AND customer_id = ?
        AND account_status = 'Active' AND balance = 0
        ''', (account[0], customer_id))

        if cursor.rowcount == 0:
            conn.rollback()
            raise ValueError("Account could not be closed")

        conn.commit()
        return True

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()



def transfer_money(customer_id, sender_account_number, receiver_account_number, amount):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        SELECT id, balance, account_status
        FROM accounts
        WHERE account_number = ? AND customer_id = ?
        ''', (sender_account_number, customer_id))

        sender_account = cursor.fetchone()

        if not sender_account:
            raise ValueError("Sender account not found")

        if sender_account[2] != "Active":
            raise ValueError("Sender account is closed")

        if not receiver_account_number:
            raise ValueError("Please enter receiver account number")

        if sender_account_number == receiver_account_number:
            raise ValueError("You cannot transfer money to the same account")

        cursor.execute('''
        SELECT id, customer_id, account_status
        FROM accounts
        WHERE account_number = ?
        ''', (receiver_account_number,))

        receiver_account = cursor.fetchone()

        if not receiver_account:
            raise ValueError("Receiver account not found")

        if receiver_account[2] != "Active":
            raise ValueError("Receiver account is closed")

        if amount <= 0:
            raise ValueError("Enter a valid transfer amount")

        if sender_account[1] < amount:
            raise ValueError("Insufficient funds")

        cursor.execute('''
        UPDATE accounts
        SET balance = balance - ?
        WHERE id = ? AND customer_id = ?
        AND balance >= ? AND account_status = 'Active'
        ''', (amount, sender_account[0], customer_id, amount))

        if cursor.rowcount == 0:
            conn.rollback()
            raise ValueError("Insufficient funds or sender account unavailable")

        cursor.execute('''
        INSERT INTO transactions
        (customer_id, account_id, account_number, transaction_type, amount)
        VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, sender_account[0], sender_account_number, "Transfer Out", amount))

        cursor.execute('''
        UPDATE accounts
        SET balance = balance + ?
        WHERE id = ? AND account_status = 'Active'
        ''', (amount, receiver_account[0]))

        if cursor.rowcount == 0:
            conn.rollback()
            raise ValueError("Receiver account unavailable. Transfer cancelled")

        cursor.execute('''
        INSERT INTO transactions
        (customer_id, account_id, account_number, transaction_type, amount)
        VALUES (?, ?, ?, ?, ?)
        ''', (receiver_account[1], receiver_account[0],
              receiver_account_number, "Transfer In", amount))

        cursor.execute('''
        SELECT balance FROM accounts
        WHERE id = ?
        ''', (sender_account[0],))

        new_balance = cursor.fetchone()[0]

        conn.commit()
        return new_balance

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()



def view_account_details(customer_id, account_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        account_number = account_number.strip()

        if not account_number:
            raise ValueError("Please enter an account number")

        cursor.execute('''
        SELECT customers.name, accounts.account_number,
        accounts.balance, accounts.account_status, accounts.created_at
        FROM accounts
        JOIN customers
        ON accounts.customer_id = customers.id
        WHERE accounts.account_number = ? AND accounts.customer_id = ?
        ''', (account_number, customer_id))

        account = cursor.fetchone()

        if not account:
            raise ValueError("Account not found")

        return account

    except sqlite3.Error:
        raise

    finally:
        conn.close()



def admin_view_account():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT customers.name,
                   accounts.account_number,
                   accounts.balance,
                   accounts.account_status,
                   accounts.created_at
            FROM accounts
            JOIN customers ON accounts.customer_id = customers.id
            ORDER BY accounts.id ASC
        ''')

        return cursor.fetchall()

    except sqlite3.Error:
        raise

    finally:
        conn.close()



def admin_search_account(account_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        account_number = account_number.strip()

        if not account_number:
            raise ValueError("Please enter an account number.")

        cursor.execute('''
            SELECT customers.name,
                   accounts.account_number,
                   accounts.balance,
                   accounts.account_status,
                   accounts.created_at
            FROM accounts
            JOIN customers ON accounts.customer_id = customers.id
            WHERE accounts.account_number = ?
        ''', (account_number,))

        return cursor.fetchone()

    except sqlite3.Error:
        raise

    finally:
        conn.close()



def admin_close_account(account_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        account_number = account_number.strip()

        if not account_number:
            raise ValueError("Please enter an account number.")

        cursor.execute('''
            SELECT customers.name,
                   accounts.account_number,
                   accounts.balance,
                   accounts.account_status,
                   accounts.created_at
            FROM accounts
            JOIN customers ON accounts.customer_id = customers.id
            WHERE accounts.account_number = ?
        ''', (account_number,))

        account = cursor.fetchone()

        if not account:
            raise ValueError("Bank account not found.")

        if account[2] != 0:
            raise ValueError(
                "Bank account contains funds. Please empty it before closing."
            )

        if account[3] == "Closed":
            raise ValueError("Bank account is already closed.")

        cursor.execute('''
            UPDATE accounts
            SET account_status = 'Closed'
            WHERE account_number = ?
            AND account_status = 'Active'
            AND balance = 0
        ''', (account_number,))

        if cursor.rowcount == 0:
            raise ValueError("Account could not be closed.")

        conn.commit()
        return True

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()



def admin_reactivate_account(account_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        account_number = account_number.strip()

        if not account_number:
            raise ValueError("Please enter an account number.")

        cursor.execute('''
            SELECT account_status
            FROM accounts
            WHERE account_number = ?
        ''', (account_number,))

        account = cursor.fetchone()

        if not account:
            raise ValueError("Bank account not found.")

        if account[0] != "Closed":
            raise ValueError("Account is already active.")

        cursor.execute('''
            UPDATE accounts
            SET account_status = 'Active'
            WHERE account_number = ?
            AND account_status = 'Closed'
        ''', (account_number,))

        if cursor.rowcount == 0:
            raise ValueError("Account could not be reactivated.")

        conn.commit()
        return True

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()



def admin_dashboard_stats():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM accounts")
        total_accounts = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM accounts WHERE account_status = ?",
            ("Active",)
        )
        active_accounts = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM accounts WHERE account_status = ?",
            ("Closed",)
        )
        closed_accounts = cursor.fetchone()[0]

        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE transaction_type = ?",
            ("Deposit",)
        )
        total_deposits = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE transaction_type = ?",
            ("Withdraw",)
        )
        total_withdrawals = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE transaction_type = ?",
            ("Transfer Out",)
        )
        total_transfer_out = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE transaction_type = ?",
            ("Transfer In",)
        )
        total_transfer_in = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT SUM(balance) FROM accounts WHERE account_status = ?",
            ("Active",)
        )
        total_balance = cursor.fetchone()[0] or 0

        return {
            "total_customers": total_customers,
            "total_accounts": total_accounts,
            "active_accounts": active_accounts,
            "closed_accounts": closed_accounts,
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals,
            "total_transfer_out": total_transfer_out,
            "total_transfer_in": total_transfer_in,
            "total_balance": total_balance
        }

    except sqlite3.Error:
        raise

    finally:
        conn.close()



def admin_view_transactions():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT transactions.id,
                   customers.name,
                   transactions.account_number,
                   transactions.transaction_type,
                   transactions.amount,
                   transactions.timestamp
            FROM transactions
            JOIN customers ON transactions.customer_id = customers.id
            ORDER BY transactions.timestamp DESC
        ''')

        return cursor.fetchall()

    except sqlite3.Error:
        raise

    finally:
        conn.close()



def admin_search_transaction(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        transaction_id = str(transaction_id).strip()

        if not transaction_id:
            raise ValueError("Please enter a transaction ID.")

        if not transaction_id.isdigit() or int(transaction_id) <= 0:
            raise ValueError("Transaction ID must be a positive number.")

        cursor.execute('''
            SELECT transactions.id,
                   customers.name,
                   transactions.customer_id,
                   transactions.account_number,
                   transactions.transaction_type,
                   transactions.amount,
                   transactions.timestamp
            FROM transactions
            JOIN customers ON transactions.customer_id = customers.id
            WHERE transactions.id = ?
        ''', (int(transaction_id),))

        return cursor.fetchone()

    except sqlite3.Error:
        raise

    finally:
        conn.close()



def admin_filter_transactions(transaction_type):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        transaction_types = {
            "Deposit",
            "Withdraw",
            "Transfer In",
            "Transfer Out",
            "All Transactions"
        }

        if transaction_type not in transaction_types:
            raise ValueError("Invalid transaction type.")

        if transaction_type == "All Transactions":
            cursor.execute('''
                SELECT transactions.id,
                       customers.name,
                       transactions.account_number,
                       transactions.transaction_type,
                       transactions.amount,
                       transactions.timestamp
                FROM transactions
                JOIN customers ON transactions.customer_id = customers.id
                ORDER BY transactions.timestamp DESC
            ''')

        else:
            cursor.execute('''
                SELECT transactions.id,
                       customers.name,
                       transactions.account_number,
                       transactions.transaction_type,
                       transactions.amount,
                       transactions.timestamp
                FROM transactions
                JOIN customers ON transactions.customer_id = customers.id
                WHERE transactions.transaction_type = ?
                ORDER BY transactions.timestamp DESC
            ''', (transaction_type,))

        return cursor.fetchall()

    except sqlite3.Error:
        raise

    finally:
        conn.close()



def admin_filter_transaction_by_date(start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        start_date = start_date.strip()
        end_date = end_date.strip()

        if not start_date or not end_date:
            raise ValueError("Please enter both dates.")

        try:
            start_date = datetime.strptime(
                start_date, "%Y-%m-%d"
            ).date()

            end_date = datetime.strptime(
                end_date, "%Y-%m-%d"
            ).date()

        except ValueError:
            raise ValueError("Invalid date. Use YYYY-MM-DD.")

        if start_date > end_date:
            raise ValueError("Start date cannot be after end date.")

        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        cursor.execute('''
            SELECT transactions.id,
                   customers.name,
                   transactions.account_number,
                   transactions.transaction_type,
                   transactions.amount,
                   transactions.timestamp
            FROM transactions
            JOIN customers ON transactions.customer_id = customers.id
            WHERE DATE(transactions.timestamp) BETWEEN ? AND ?
            ORDER BY transactions.timestamp DESC
        ''', (start_date, end_date))

        return cursor.fetchall()

    except sqlite3.Error:
        raise

    finally:
        conn.close()




def admin_transaction_summary(start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        start_date = start_date.strip()
        end_date = end_date.strip()

        if not start_date or not end_date:
            raise ValueError("Please enter both dates.")

        try:
            start_date = datetime.strptime(
                start_date, "%Y-%m-%d"
            ).date()

            end_date = datetime.strptime(
                end_date, "%Y-%m-%d"
            ).date()

        except ValueError:
            raise ValueError("Invalid date. Use YYYY-MM-DD.")

        if start_date > end_date:
            raise ValueError("Start date cannot be after end date.")

        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        cursor.execute('''
            SELECT COUNT(*)
            FROM transactions
            WHERE DATE(timestamp) BETWEEN ? AND ?
        ''', (start_date, end_date))

        total_transactions = cursor.fetchone()[0]

        transaction_types = [
            "Deposit",
            "Withdraw",
            "Transfer In",
            "Transfer Out"
        ]

        totals = {}

        for transaction_type in transaction_types:
            cursor.execute('''
                SELECT SUM(amount)
                FROM transactions
                WHERE transaction_type = ?
                AND DATE(timestamp) BETWEEN ? AND ?
            ''', (transaction_type, start_date, end_date))

            totals[transaction_type] = cursor.fetchone()[0] or 0

        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_transactions": total_transactions,
            "total_deposits": totals["Deposit"],
            "total_withdrawals": totals["Withdraw"],
            "total_transfer_in": totals["Transfer In"],
            "total_transfer_out": totals["Transfer Out"]
        }

    except sqlite3.Error:
        raise

    finally:
        conn.close()






def generate_account_statement(customer_id, account_number, start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        account_number = account_number.strip()
        start_date = start_date.strip()
        end_date = end_date.strip()

        if not account_number or not start_date or not end_date:
            raise ValueError("Please fill in all fields")

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        except ValueError:
            raise ValueError("Invalid date. Use YYYY-MM-DD")

        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")

        cursor.execute('''
        SELECT id, balance, created_at
        FROM accounts
        WHERE account_number = ? AND customer_id = ?
        ''', (account_number, customer_id))

        account = cursor.fetchone()

        if not account:
            raise ValueError("Invalid account number")

        account_creation_date = datetime.strptime(
            account[2], "%Y-%m-%d %H:%M:%S"
        ).date()

        if start_date < account_creation_date:
            raise ValueError("Statement cannot start before account creation")

        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        cursor.execute('''
        SELECT COALESCE(SUM(
            CASE
                WHEN transaction_type IN ('Withdraw', 'Transfer Out') THEN amount
                WHEN transaction_type IN ('Deposit', 'Transfer In') THEN -amount
                ELSE 0
            END
        ), 0)
        FROM transactions
        WHERE account_id = ? AND customer_id = ?
        AND DATE(timestamp) > ?
        ''', (account[0], customer_id, end_date))

        later_net_change = cursor.fetchone()[0]
        closing_balance = account[1] - later_net_change

        cursor.execute('''
        SELECT transaction_type, SUM(amount)
        FROM transactions
        WHERE account_id = ? AND customer_id = ?
        AND DATE(timestamp) BETWEEN ? AND ?
        GROUP BY transaction_type
        ''', (account[0], customer_id, start_date, end_date))

        totals = dict(cursor.fetchall())

        deposits = totals.get("Deposit", 0)
        withdrawals = totals.get("Withdraw", 0)
        transfer_in = totals.get("Transfer In", 0)
        transfer_out = totals.get("Transfer Out", 0)

        net_change = deposits + transfer_in - withdrawals - transfer_out
        opening_balance = closing_balance - net_change

        cursor.execute('''
        SELECT id, transaction_type, amount, timestamp
        FROM transactions
        WHERE account_id = ? AND customer_id = ?
        AND DATE(timestamp) BETWEEN ? AND ?
        ORDER BY timestamp ASC
        ''', (account[0], customer_id, start_date, end_date))

        transactions = cursor.fetchall()

        return {
            "account_number": account_number,
            "start_date": start_date,
            "end_date": end_date,
            "opening_balance": opening_balance,
            "deposits": deposits,
            "withdrawals": withdrawals,
            "transfer_in": transfer_in,
            "transfer_out": transfer_out,
            "closing_balance": closing_balance,
            "transactions": transactions
        }

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()



