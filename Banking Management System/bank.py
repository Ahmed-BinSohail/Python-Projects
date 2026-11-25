import email
import sqlite3

from database import connect_db
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
import secrets

ph = PasswordHasher()

def register_customer():
    conn = connect_db()
    cursor = conn.cursor()
    name = input("Name: ").strip()
    if not name:
        print("Please enter your name")
        conn.close()
        return
    if not all(character.isalpha() or character in " -'" for character in name):
        print("Please enter a valid name")
        conn.close()
        return
    email = input("Email: ").strip()
    if not email:
        print("Please enter an email")
        conn.close()
        return
    at_pos = email.find('@')
    dot_pos = email.find('.', at_pos)
    if at_pos <= 0 or dot_pos <= at_pos + 1 or dot_pos == len(email) - 1:
        print("Invalid Email")
        conn.close()
        return
    cursor.execute("SELECT id FROM customers WHERE email = ?", (email,))
    if cursor.fetchone():
        print("This email is already registered.")
        conn.close()
        return
    phone = input("Phone Number: ").strip()
    if not phone:
        print("Please enter your phone number")
        conn.close()
        return
    if not phone.isdigit():
        print("Invalid Phone Number")
        conn.close()
        return
    if len(phone) != 11:
        print("Phone number must be 11 digits")
        conn.close()
        return
    password = input("Create a Password: ")
    if not password:
        print("Please enter your password")
        conn.close()
        return
    if len(password) < 8:
        print("Password must be at least 8 characters")
        conn.close()
        return
    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
            break
    if not has_digit:
        print("Password must contain at least one digit")
        conn.close()
        return
    confirm_password = input("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match")
        conn.close()
        return
    try:
        password_hash = ph.hash(password)
        cursor.execute('''
        INSERT INTO customers (name, email, password_hash, phone)
        VALUES (?, ?, ?, ?)
        ''', (name, email, password_hash, phone))
        customer_id = cursor.lastrowid
        conn.commit()
        print("Registration Successful")
        return customer_id


    except sqlite3.IntegrityError:

        print("This email is already registered.")


    except sqlite3.Error as e:

        print("Database error:", e)


    finally:

        conn.close()


def view_customers():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT id, name, email, phone
            FROM customers
            ORDER BY id ASC
        ''')

        customers = cursor.fetchall()
        return customers

    except sqlite3.Error:
        raise

    finally:
        conn.close()



def update_customer(email, password, new_phone):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        email = email.strip()
        new_phone = new_phone.strip()

        if not email or not password or not new_phone:
            raise ValueError("All fields are required.")

        if not new_phone.isdigit():
            raise ValueError("Phone number must contain digits only.")

        if len(new_phone) != 11:
            raise ValueError("Phone number must be 11 digits.")

        cursor.execute('''
            SELECT id, password_hash
            FROM customers
            WHERE email = ?
        ''', (email,))

        customer = cursor.fetchone()

        if not customer:
            raise ValueError("Invalid email or password.")

        try:
            ph.verify(customer[1], password)
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            raise ValueError("Invalid email or password.")

        cursor.execute('''
            UPDATE customers
            SET phone = ?
            WHERE id = ?
        ''', (new_phone, customer[0]))

        if cursor.rowcount == 0:
            raise ValueError("No customer was updated.")

        conn.commit()
        return True

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()


def delete_customer(email, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        email = email.strip()

        if not email or not password:
            raise ValueError("Email and password are required.")

        cursor.execute('''
            SELECT id, password_hash
            FROM customers
            WHERE email = ?
        ''', (email,))

        customer = cursor.fetchone()

        if not customer:
            raise ValueError("Invalid email or password.")

        try:
            ph.verify(customer[1], password)
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            raise ValueError("Invalid email or password.")

        cursor.execute('''
            DELETE FROM customers
            WHERE id = ?
        ''', (customer[0],))

        if cursor.rowcount == 0:
            raise ValueError("Customer not found or already deleted.")

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError(
            "Cannot delete customer. A bank account is linked to this customer."
        )

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()


def login_customer(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT id, name, password_hash FROM customers WHERE email = ?''', (email,))
        customer = cursor.fetchone()
        if not customer:
            return None
        ph.verify(customer[2], password)
        return customer[0]
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return None
    except sqlite3.Error as e:
        raise
    finally:
        conn.close()

def create_admin():
    conn = connect_db()
    cursor = conn.cursor()
    username = input("Enter username: ").strip()
    if not username:
        print("Please enter an username")
        conn.close()
        return
    password = input("Create a Password: ")
    if not password:
        print("Please enter your password")
        conn.close()
        return
    if len(password) < 8:
        print("Password must be at least 8 characters")
        conn.close()
        return
    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
            break
    if not has_digit:
        print("Password must contain at least one digit")
        conn.close()
        return
    confirm_password = input("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match")
        conn.close()
        return
    try:
        password_hash = ph.hash(password)
        cursor.execute('''
        INSERT INTO admins (username, password_hash)
        VALUES (?, ?)
        ''', (username, password_hash))
        conn.commit()
        print("Registration Successful")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print("This username is already taken")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def login_admin(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        username = username.strip()

        if not username or not password:
            return None

        cursor.execute(
            '''SELECT id, username, password_hash
               FROM admins
               WHERE username = ?''',
            (username,)
        )

        admin = cursor.fetchone()

        if not admin:
            return None

        ph.verify(admin[2], password)

        return admin[0]

    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return None

    except sqlite3.Error:
        raise

    finally:
        conn.close()




def change_password(customer_id, current_password, new_password, confirmed_password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        if not current_password:
            raise ValueError("Please enter your current password")

        if not new_password:
            raise ValueError("Please enter a new password")

        if len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters")

        has_digit = False

        for char in new_password:
            if char.isdigit():
                has_digit = True
                break

        if not has_digit:
            raise ValueError("Password must contain at least one digit")

        if not confirmed_password:
            raise ValueError("Please confirm your new password")

        if new_password != confirmed_password:
            raise ValueError("Passwords do not match")

        cursor.execute('''
        SELECT password_hash
        FROM customers
        WHERE id = ?
        ''', (customer_id,))

        result = cursor.fetchone()

        if not result:
            raise ValueError("User not found")

        try:
            ph.verify(result[0], current_password)

        except (VerifyMismatchError, VerificationError, InvalidHashError):
            raise ValueError("Invalid current password")

        try:
            ph.verify(result[0], new_password)
            raise ValueError(
                "New password must be different from your current password"
            )

        except VerifyMismatchError:
            pass

        except (VerificationError, InvalidHashError):
            raise ValueError("Unable to verify your current password")

        password_hash = ph.hash(new_password)

        cursor.execute('''
        UPDATE customers
        SET password_hash = ?
        WHERE id = ?
        ''', (password_hash, customer_id))

        if cursor.rowcount == 0:
            raise ValueError("Password update failed. User not found.")

        conn.commit()
        return True

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()





def forget_password(email, verification_code, entered_code, new_password, confirmed_password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        email = email.strip()
        entered_code = entered_code.strip()

        if not email:
            raise ValueError("Please enter your email")

        cursor.execute('''
        SELECT id, email, password_hash
        FROM customers
        WHERE email = ?
        ''', (email,))

        customer = cursor.fetchone()

        if not customer:
            raise ValueError("User not found")

        if len(entered_code) != 6 or not entered_code.isdigit():
            raise ValueError("Please enter a valid six-digit code")

        if entered_code != verification_code:
            raise ValueError("Incorrect verification code")

        if not new_password:
            raise ValueError("Please enter a new password")

        if len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters")

        has_digit = False

        for char in new_password:
            if char.isdigit():
                has_digit = True
                break

        if not has_digit:
            raise ValueError("Password must contain at least one digit")

        if not confirmed_password:
            raise ValueError("Please confirm your password")

        if new_password != confirmed_password:
            raise ValueError("Passwords do not match")

        try:
            ph.verify(customer[2], new_password)

            raise ValueError(
                "New password must be different from your current password"
            )

        except VerifyMismatchError:
            pass

        except (VerificationError, InvalidHashError):
            raise ValueError("Unable to verify the current password")

        password_hash = ph.hash(new_password)

        cursor.execute('''
        UPDATE customers
        SET password_hash = ?
        WHERE id = ?
        ''', (password_hash, customer[0]))

        if cursor.rowcount == 0:
            raise ValueError("Password reset failed")

        conn.commit()
        return True

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()




def view_my_profile(customer_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        SELECT id, name, email, phone
        FROM customers
        WHERE id = ?
        ''', (customer_id,))

        customer_info = cursor.fetchone()
        return customer_info

    except sqlite3.Error:
        raise

    finally:
        conn.close()




def update_profile(customer_id, field, new_value):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        new_value = new_value.strip()

        if not new_value:
            raise ValueError("Please enter a value")

        if field == "Name":
            if not all(char.isalpha() or char in " -'" for char in new_value):
                raise ValueError("Please enter a valid name")

            column = "name"

        elif field == "Email":
            at_pos = new_value.find('@')
            dot_pos = new_value.find('.', at_pos)

            if at_pos <= 0 or dot_pos <= at_pos + 1 or dot_pos == len(new_value) - 1:
                raise ValueError("Invalid email address")

            column = "email"

        elif field == "Phone":
            if not new_value.isdigit() or len(new_value) != 11:
                raise ValueError("Phone number must be exactly 11 digits")

            column = "phone"

        else:
            raise ValueError("Invalid profile field")

        cursor.execute(
            f"UPDATE customers SET {column} = ? WHERE id = ?",
            (new_value, customer_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Customer not found")

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError("This email is already registered")

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()



def add_admin(username, password, confirm_password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        username = username.strip()

        if not username:
            raise ValueError("Please enter a username.")

        if not password:
            raise ValueError("Please enter a password.")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")

        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit.")

        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        password_hash = ph.hash(password)

        cursor.execute('''
            INSERT INTO admins (username, password_hash)
            VALUES (?, ?)
        ''', (username, password_hash))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError("Username already exists.")

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()


def search_customer(search_value):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        search_value = search_value.strip()

        if not search_value:
            raise ValueError("Please enter a customer ID, name, or email.")

        cursor.execute('''
            SELECT id, name, email, phone
            FROM customers
            WHERE CAST(id AS TEXT) = ?
               OR name LIKE ?
               OR email LIKE ?
            ORDER BY id ASC
        ''', (
            search_value,
            f"%{search_value}%",
            f"%{search_value}%"
        ))

        return cursor.fetchall()

    except sqlite3.Error:
        raise

    finally:
        conn.close()



