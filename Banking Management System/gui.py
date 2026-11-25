import tkinter as tk
from tkinter import messagebox, ttk
from bank import login_customer, view_my_profile, update_profile, change_password, forget_password, login_admin, view_customers, search_customer, update_customer, delete_customer, add_admin
from account import view_my_accounts, create_account, deposit_money, withdraw_money, transfer_money, view_transaction_history, check_balance, close_account,view_account_details, generate_account_statement, admin_view_account, admin_search_account,admin_close_account,admin_reactivate_account, admin_dashboard_stats,admin_view_transactions, admin_search_transaction,admin_filter_transactions,admin_filter_transaction_by_date,admin_transaction_summary
import sqlite3
from database import connect_db
import secrets

BG = "#202B3C"
CARD = "#2B394B"
PRIMARY = "#10B981"
ACCENT = "#A7F3D0"
TEXT = "#F1F5F9"
SECONDARY = "#475569"
DANGER = "#B91C1C"

root = tk.Tk()
root.title("Banking Management System")
root.geometry("1100x700")
root.configure(bg=BG)

dashboard_title = None
welcome_label = None
dashboard_frame = None

heading = tk.Label(
    root,
    text="Welcome to Banking Management System",
    font=("Arial", 24, "bold"),
    fg="#FFFFFF",
    bg="#202B3C"
)
heading.pack(pady=40)

subtitle = tk.Label(
    root,
    text= "Secure Banking. Simple Experience.",
    font=("Arial", 12),
    fg = "#A7F3D0",
    bg = "#202B3C"
)
subtitle.pack()

login_frame = tk.Frame(root,
                       bg="#2B394B",
                       width=450,
                       height=450,)
login_frame.pack(pady=35)
login_frame.pack_propagate(False)

login_title = tk.Label(
    login_frame,
    text="Welcome Back",
font=("Arial", 20, "bold"),
    fg = "#FFFFFF",
    bg = "#2B394B"
)
login_title.pack(pady=30)

email_label = tk.Label(
    login_frame,
    text="Email Address or Admin username",
    font=("Arial", 12),
    fg = "#A7F3D0",
    bg = "#2B394B"
)
email_label.pack(anchor="w", padx=40)

def clear_email_placeholder(event):
    if email_entry.get() == "Enter your email":
        email_entry.delete(0, tk.END)

def restore_email_placeholder(event):
    if email_entry.get() == "":
        email_entry.insert(0, "Enter your email or admin username")

def clear_password_placeholder(event):
    if password_entry.get() == "Enter your password":
        password_entry.delete(0, tk.END)
        password_entry.config(show="*")

def restore_password_placeholder(event):
    if password_entry.get() == "":
        password_entry.config(show="")
        password_entry.insert(0, "Enter your password")

def toggle_password():
    if password_entry.cget("show")=="*":
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

email_placeholder = "Enter email address or admin username"

email_entry = tk.Entry(
    login_frame,
    font=("Arial", 12),
    width=35,
    bg="#1E293b",
    fg="#FFFFFF",
    insertbackground="#FFFFFF",
    relief="flat"
)

email_entry.insert(0, email_placeholder)
email_entry.pack(pady=10, ipady=8)


def clear_email_placeholder(event):
    if email_entry.get() == email_placeholder:
        email_entry.delete(0, tk.END)


def restore_email_placeholder(event):
    if not email_entry.get().strip():
        email_entry.insert(0, email_placeholder)


email_entry.bind("<FocusIn>", clear_email_placeholder)
email_entry.bind("<FocusOut>", restore_email_placeholder)


def email_focus_in(event):
    if email_entry.get() == email_placeholder:
        email_entry.delete(0, tk.END)
        email_entry.config(fg=TEXT)


def email_focus_out(event):
    if not email_entry.get().strip():
        email_entry.insert(0, email_placeholder)
        email_entry.config(fg="#94A3B8")


email_entry.bind("<FocusIn>", email_focus_in)
email_entry.bind("<FocusOut>", email_focus_out)


def email_focus_in(event):
    if email_entry.get() == email_placeholder:
        email_entry.delete(0, tk.END)
        email_entry.config(fg=TEXT)


def email_focus_out(event):
    if not email_entry.get().strip():
        email_entry.delete(0, tk.END)
        email_entry.insert(0, email_placeholder)
        email_entry.config(fg="#94A3B8")


email_entry.bind("<FocusIn>", email_focus_in)
email_entry.bind("<FocusOut>", email_focus_out)

passwrod_label = tk.Label(
    login_frame,
    text="Password",
    font=("Arial", 12),
    fg = "#A7F3D0",
    bg = "#2B394B"
)
passwrod_label.pack(anchor="w", padx=40)

password_entry = tk.Entry(
    login_frame,
    font=("Arial", 12),
    width=35,
    bg = "#1E293b",
    fg = "#FFFFFF",
    insertbackground="#FFFFFF",
    relief="flat"
)
password_entry.insert(0, "Enter your password")
password_entry.config(show="")
password_entry.pack(pady=10, ipady=8)
password_entry.bind("<FocusIn>", clear_password_placeholder)
password_entry.bind("<FocusOut>", restore_password_placeholder)

show_password = tk.Checkbutton(
    login_frame,
    text="Show Password",
    font=("Arial", 8),
    bg = "#2B394B",
    fg = "#A7F3D0",
    activebackground="#2B394B",
    activeforeground="#FFFFFF",
    selectcolor="#1E293B",
    cursor="hand2",
    command = toggle_password
)

show_password.pack(anchor="w", padx=40)

forgot_password = tk.Label(
    login_frame,
    text="Forgot Password",
    font=("Arial", 8),
    fg="#60A5FA",
    bg = "#2B394B",
    cursor="hand2"
)

forgot_password.pack(anchor="e", padx=40, pady=5)


def show_accounts(customer_id):
    accounts = view_my_accounts(customer_id)

    if not accounts:
        messagebox.showinfo(
            "My Accounts",
            "You dont have any bank accounts yet."
        )
        return
    accounts_window = tk.Toplevel(root)
    accounts_window.title("My Accounts")
    accounts_window.geometry("600x400")
    accounts_window.configure(bg="#202B3C")

    title = tk.Label(
        accounts_window,
        text="My Bank Accounts",
        font=("Arial", 22, "bold"),
        fg="#FFFFFF",
        bg="#202B3C"
    )
    title.pack(pady=25)

    for acc in accounts:
        account_card = tk.Frame(
            accounts_window,
            bg="#2B394B",
            padx=20,
            pady=15
        )
        account_card.pack(fill="x", padx=30, pady=10)

        account_number = tk.Label(
            account_card,
            text=f"Account Number: {acc[0]}",
            font=("Arial", 12, "bold"),
            fg="#FFFFFF",
            bg="#2B394B"
        )
        account_number.pack(anchor="w")

        balance = tk.Label(
            account_card,
            text=f"Balance: Rs. {acc[1]:,}",
            font=("Arial", 12),
            fg="#A7F3D0",
            bg="#2B394B"
        )
        balance.pack(anchor="w", pady=5)

        status = tk.Label(
            account_card,
            text=f"Status: {acc[2]}",
            font=("Arial", 10),
            fg="#60A5FA",
            bg="#2B394B"
        )
        status.pack(anchor="w")

    close_button = tk.Button(
        accounts_window,
        text="Close",
        font=("Arial", 11, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=15,
        pady=8,
        command=accounts_window.destroy
    )
    close_button.pack(pady=20)

def show_create_account(customer_id):
    confirm = messagebox.askyesno(
        "Create Account",
        "Would you like to create a new bank account?"
    )

    if not confirm:
        return

    try:
        account_number = create_account(customer_id)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return

    if account_number is None:
        messagebox.showerror(
            "Account Creation Failed",
            "Could not create your account. Please try again."
        )
        return

    messagebox.showinfo(
        "Account Created",
        f"Your new account has been created!\n\n"
        f"Account Number: {account_number}"
    )

def show_deposit(customer_id):
    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit Money")
    deposit_window.geometry("450x400")
    deposit_window.configure(bg="#202B3C")

    title = tk.Label(
        deposit_window,
        text="Deposit Money",
        font=("Arial", 22, "bold"),
        fg="#FFFFFF",
        bg="#202B3C"
    )
    title.pack(pady=25)

    account_label = tk.Label(
        deposit_window,
        text="Account Number",
        font=("Arial", 12),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    account_label.pack(pady=5)

    account_entry = tk.Entry(
        deposit_window,
        font=("Arial", 12),
        width=30
    )
    account_entry.pack(pady=10, ipady=7)

    amount_label = tk.Label(
        deposit_window,
        text="Amount",
        font=("Arial", 12),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    amount_label.pack(pady=5)

    amount_entry = tk.Entry(
        deposit_window,
        font=("Arial", 12),
        width=30
    )
    amount_entry.pack(pady=10, ipady=7)

    def make_deposit():
        account_number = account_entry.get().strip()
        amount = amount_entry.get().strip()

        if not account_number or not amount:
            messagebox.showerror(
                "Input Error",
                "Please fill in all fields."
            )
            return

        try:
            amount = int(amount)

            new_balance = deposit_money(
                customer_id,
                account_number,
                amount
            )

        except ValueError as e:
            messagebox.showerror("Deposit Failed", str(e))
            return

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return

        messagebox.showinfo(
            "Deposit Successful",
            f"Money deposited successfully!\n\n"
            f"New Balance: Rs. {new_balance:,}"
        )

        deposit_window.destroy()

    deposit_button = tk.Button(
        deposit_window,
        text="Confirm Deposit",
        font=("Arial", 12, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        activebackground="#0F766E",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=25,
        pady=10,
        command=make_deposit
    )
    deposit_button.pack(pady=25)

def show_withdraw(customer_id):
    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("450x400")
    withdraw_window.configure(bg="#202B3C")

    title = tk.Label(
        withdraw_window,
        text="Withdraw Money",
        font=("Arial", 22, "bold"),
        fg="#FFFFFF",
        bg="#202B3C"
    )
    title.pack(pady=25)

    account_label = tk.Label(
        withdraw_window,
        text="Account Number",
        font=("Arial", 12),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    account_label.pack(pady=5)

    account_entry = tk.Entry(
        withdraw_window,
        font=("Arial", 12),
        width=30
    )
    account_entry.pack(pady=10, ipady=7)

    amount_label = tk.Label(
        withdraw_window,
        text="Amount",
        font=("Arial", 12),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    amount_label.pack(pady=5)

    amount_entry = tk.Entry(
        withdraw_window,
        font=("Arial", 12),
        width=30
    )
    amount_entry.pack(pady=10, ipady=7)

    def make_withdrawal():
        account_number = account_entry.get().strip()
        amount = amount_entry.get().strip()

        if not account_number or not amount:
            messagebox.showerror(
                "Input Error",
                "Please fill in all fields."
            )
            return

        try:
            amount = int(amount)

            new_balance = withdraw_money(
                customer_id,
                account_number,
                amount
            )

        except ValueError as e:
            messagebox.showerror("Withdrawal Failed", str(e))
            return

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return

        messagebox.showinfo(
            "Withdrawal Successful",
            f"Money withdrawn successfully!\n\n"
            f"Remaining Balance: Rs. {new_balance:,}"
        )

        withdraw_window.destroy()

    withdraw_button = tk.Button(
        withdraw_window,
        text="Confirm Withdrawal",
        font=("Arial", 12, "bold"),
        bg="#DC2626",
        fg="#FFFFFF",
        activebackground="#B91C1C",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=25,
        pady=10,
        command=make_withdrawal
    )
    withdraw_button.pack(pady=25)

def show_transfer(customer_id):
    transfer_window = tk.Toplevel(root)
    transfer_window.title("Transfer Money")
    transfer_window.geometry("480x520")
    transfer_window.configure(bg="#202B3C")

    title = tk.Label(
        transfer_window,
        text="Transfer Money",
        font=("Arial", 22, "bold"),
        fg="#FFFFFF",
        bg="#202B3C"
    )
    title.pack(pady=25)

    sender_label = tk.Label(
        transfer_window,
        text="Your Account Number",
        font=("Arial", 12),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    sender_label.pack(pady=5)

    sender_entry = tk.Entry(
        transfer_window,
        font=("Arial", 12),
        width=30
    )
    sender_entry.pack(pady=10, ipady=7)

    receiver_label = tk.Label(
        transfer_window,
        text="Receiver Account Number",
        font=("Arial", 12),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    receiver_label.pack(pady=5)

    receiver_entry = tk.Entry(
        transfer_window,
        font=("Arial", 12),
        width=30
    )
    receiver_entry.pack(pady=10, ipady=7)

    amount_label = tk.Label(
        transfer_window,
        text="Amount",
        font=("Arial", 12),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    amount_label.pack(pady=5)

    amount_entry = tk.Entry(
        transfer_window,
        font=("Arial", 12),
        width=30
    )
    amount_entry.pack(pady=10, ipady=7)

    def make_transfer():
        sender_account = sender_entry.get().strip()
        receiver_account = receiver_entry.get().strip()
        amount = amount_entry.get().strip()

        if not sender_account or not receiver_account or not amount:
            messagebox.showerror(
                "Input Error",
                "Please fill in all fields."
            )
            return

        try:
            amount = int(amount)

            new_balance = transfer_money(
                customer_id,
                sender_account,
                receiver_account,
                amount
            )

        except ValueError as e:
            messagebox.showerror("Transfer Failed", str(e))
            return

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return

        messagebox.showinfo(
            "Transfer Successful",
            f"Money transferred successfully!\n\n"
            f"Remaining Balance: Rs. {new_balance:,}"
        )

        transfer_window.destroy()

    transfer_button = tk.Button(
        transfer_window,
        text="Confirm Transfer",
        font=("Arial", 12, "bold"),
        bg="#475569",
        fg="#FFFFFF",
        activebackground="#6D28D9",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=25,
        pady=10,
        command=make_transfer
    )
    transfer_button.pack(pady=25)


def show_transaction_history(customer_id):
    try:
        transactions = view_transaction_history(customer_id)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return

    history_window = tk.Toplevel(root)
    history_window.title("Transaction History")
    history_window.geometry("950x550")
    history_window.configure(bg="#202B3C")

    title = tk.Label(
        history_window,
        text="Transaction History",
        font=("Arial", 24, "bold"),
        fg="#FFFFFF",
        bg="#202B3C"
    )
    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        history_window,
        text="View all your banking transactions",
        font=("Arial", 11),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    subtitle.pack(pady=(0, 20))

    if not transactions:
        empty_label = tk.Label(
            history_window,
            text="No transactions found.",
            font=("Arial", 14),
            fg="#A7F3D0",
            bg="#202B3C"
        )
        empty_label.pack(pady=60)

    else:
        table_frame = tk.Frame(
            history_window,
            bg="#2B394B"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        columns = (
            "id",
            "account",
            "type",
            "amount",
            "date"
        )

        transaction_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        transaction_table.heading("id", text="ID")
        transaction_table.heading("account", text="Account Number")
        transaction_table.heading("type", text="Transaction Type")
        transaction_table.heading("amount", text="Amount")
        transaction_table.heading("date", text="Date & Time")

        transaction_table.column("id", width=50, anchor="center")
        transaction_table.column("account", width=180, anchor="center")
        transaction_table.column("type", width=150, anchor="center")
        transaction_table.column("amount", width=130, anchor="center")
        transaction_table.column("date", width=200, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=transaction_table.yview
        )

        transaction_table.configure(
            yscrollcommand=scrollbar.set
        )

        transaction_table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=10
        )

        for transaction in transactions:
            transaction_table.insert(
                "",
                "end",
                values=(
                    transaction[0],
                    transaction[1],
                    transaction[2],
                    f"Rs. {transaction[3]:,}",
                    transaction[4]
                )
            )

    close_button = tk.Button(
        history_window,
        text="Close",
        font=("Arial", 11, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=15,
        pady=8,
        command=history_window.destroy
    )
    close_button.pack(pady=15)


def show_my_profile(customer_id):
    try:
        customer = view_my_profile(customer_id)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return

    if not customer:
        messagebox.showerror(
            "Profile",
            "Customer profile not found."
        )
        return

    profile_window = tk.Toplevel(root)
    profile_window.title("My Profile")
    profile_window.geometry("550x500")
    profile_window.configure(bg="#202B3C")

    title = tk.Label(
        profile_window,
        text="My Profile",
        font=("Arial", 25, "bold"),
        fg="#FFFFFF",
        bg="#202B3C"
    )
    title.pack(pady=(30, 5))

    subtitle = tk.Label(
        profile_window,
        text="Your personal account information",
        font=("Arial", 11),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    subtitle.pack(pady=(0, 25))

    profile_card = tk.Frame(
        profile_window,
        bg="#2B394B",
        padx=30,
        pady=25
    )
    profile_card.pack(fill="x", padx=45, pady=10)

    details = [
        ("Customer ID", customer[0]),
        ("Full Name", customer[1]),
        ("Email Address", customer[2]),
        ("Phone Number", customer[3])
    ]

    for label_text, value in details:
        label = tk.Label(
            profile_card,
            text=label_text,
            font=("Arial", 10, "bold"),
            fg="#60A5FA",
            bg="#2B394B"
        )
        label.pack(anchor="w", pady=(8, 2))

        value_label = tk.Label(
            profile_card,
            text=str(value),
            font=("Arial", 13),
            fg="#FFFFFF",
            bg="#2B394B"
        )
        value_label.pack(anchor="w", pady=(0, 8))

    close_button = tk.Button(
        profile_window,
        text="Close",
        font=("Arial", 11, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=18,
        pady=9,
        command=profile_window.destroy
    )
    close_button.pack(pady=20)


def show_update_profile(customer_id):

    try:
        customer = view_my_profile(customer_id)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return

    if not customer:
        messagebox.showerror("Profile", "Customer not found")
        return

    profile_window = tk.Toplevel(root)
    profile_window.title("Edit Profile")
    profile_window.geometry("550x550")
    profile_window.configure(bg="#202B3C")

    title = tk.Label(
        profile_window,
        text="Edit Profile",
        font=("Arial", 25, "bold"),
        fg="#FFFFFF",
        bg="#202B3C"
    )
    title.pack(pady=(30, 5))

    subtitle = tk.Label(
        profile_window,
        text="Update your personal information",
        font=("Arial", 11),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    subtitle.pack(pady=(0, 25))

    profile_card = tk.Frame(
        profile_window,
        bg="#2B394B",
        padx=30,
        pady=25
    )
    profile_card.pack(fill="x", padx=45, pady=10)

    current_details = tk.Label(
        profile_card,
        text=(
            f"Name: {customer[1]}\n"
            f"Email: {customer[2]}\n"
            f"Phone: {customer[3]}"
        ),
        font=("Arial", 11),
        fg="#A7F3D0",
        bg="#2B394B",
        justify="left"
    )
    current_details.pack(anchor="w", pady=(0, 20))

    field_label = tk.Label(
        profile_card,
        text="Select Information to Update",
        font=("Arial", 11, "bold"),
        fg="#FFFFFF",
        bg="#2B394B"
    )
    field_label.pack(anchor="w", pady=(5, 8))

    field_var = tk.StringVar(value="Name")

    field_dropdown = ttk.Combobox(
        profile_card,
        textvariable=field_var,
        values=["Name", "Email", "Phone"],
        state="readonly",
        font=("Arial", 11)
    )
    field_dropdown.pack(fill="x", pady=(0, 20))

    value_label = tk.Label(
        profile_card,
        text="Enter New Value",
        font=("Arial", 11, "bold"),
        fg="#FFFFFF",
        bg="#2B394B"
    )
    value_label.pack(anchor="w", pady=(5, 8))

    value_entry = tk.Entry(
        profile_card,
        font=("Arial", 12),
        bg="#1E293B",
        fg="#FFFFFF",
        insertbackground="#FFFFFF",
        relief="flat"
    )
    value_entry.pack(fill="x", ipady=9)

    def save_changes():
        field = field_var.get()
        new_value = value_entry.get()

        try:
            update_profile(customer_id, field, new_value)

            messagebox.showinfo(
                "Profile Updated",
                f"Your {field.lower()} has been updated successfully!"
            )

            profile_window.destroy()

        except ValueError as e:
            messagebox.showerror("Update Failed", str(e))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    save_button = tk.Button(
        profile_window,
        text="Save Changes",
        font=("Arial", 12, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        activebackground="#0F766E",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=22,
        pady=11,
        command=save_changes
    )
    save_button.pack(pady=20)

    close_button = tk.Button(
        profile_window,
        text="Cancel",
        font=("Arial", 11, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=22,
        pady=9,
        command=profile_window.destroy
    )
    close_button.pack(pady=5)


def show_check_balance(customer_id):

    balance_window = tk.Toplevel(root)
    balance_window.title("Check Balance")
    balance_window.geometry("500x480")
    balance_window.configure(bg="#202B3C")

    title = tk.Label(
        balance_window,
        text="Check Balance",
        font=("Arial", 25, "bold"),
        fg="#FFFFFF",
        bg="#202B3C"
    )
    title.pack(pady=(35, 5))

    subtitle = tk.Label(
        balance_window,
        text="View your current account balance",
        font=("Arial", 11),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    subtitle.pack(pady=(0, 30))

    balance_card = tk.Frame(
        balance_window,
        bg="#2B394B",
        padx=30,
        pady=30
    )
    balance_card.pack(fill="x", padx=40, pady=10)

    account_label = tk.Label(
        balance_card,
        text="Enter Account Number",
        font=("Arial", 11, "bold"),
        fg="#FFFFFF",
        bg="#2B394B"
    )
    account_label.pack(anchor="w", pady=(0, 10))

    account_entry = tk.Entry(
        balance_card,
        font=("Arial", 12),
        bg="#1E293B",
        fg="#FFFFFF",
        insertbackground="#FFFFFF",
        relief="flat"
    )
    account_entry.pack(fill="x", ipady=10)

    def search_balance():
        account_number = account_entry.get().strip()

        if not account_number:
            messagebox.showerror(
                "Missing Information",
                "Please enter your account number."
            )
            return

        try:
            account = check_balance(customer_id, account_number)

            messagebox.showinfo(
                "Account Balance",
                f"Account Number: {account[0]}\n\n"
                f"Available Balance: Rs. {account[1] / 100:,.2f}\n\n"
                f"Status: {account[2]}"
            )

        except ValueError as e:
            messagebox.showerror("Balance Lookup Failed", str(e))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    search_button = tk.Button(
        balance_card,
        text="Check Balance",
        font=("Arial", 12, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        activebackground="#0F766E",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=25,
        pady=11,
        command=search_balance
    )
    search_button.pack(pady=(25, 5))

    close_button = tk.Button(
        balance_window,
        text="Close",
        font=("Arial", 11, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=20,
        pady=9,
        command=balance_window.destroy
    )
    close_button.pack(pady=20)


def show_close_account(customer_id):

    close_window = tk.Toplevel(root)
    close_window.title("Close Bank Account")
    close_window.geometry("500x450")
    close_window.configure(bg="#202B3C")

    title = tk.Label(
        close_window,
        text="Close Bank Account",
        font=("Arial", 24, "bold"),
        fg="#FFFFFF",
        bg="#202B3C"
    )
    title.pack(pady=(35, 10))

    subtitle = tk.Label(
        close_window,
        text="Permanently close your selected bank account",
        font=("Arial", 11),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    subtitle.pack(pady=(0, 25))

    account_card = tk.Frame(
        close_window,
        bg="#2B394B",
        padx=30,
        pady=30
    )
    account_card.pack(fill="x", padx=40, pady=10)

    warning = tk.Label(
        account_card,
        text="Important: Your account balance must be zero before closing.",
        font=("Arial", 10),
        fg="#FCA5A5",
        bg="#2B394B",
        wraplength=350,
        justify="left"
    )
    warning.pack(anchor="w", pady=(0, 20))

    account_label = tk.Label(
        account_card,
        text="Account Number",
        font=("Arial", 11, "bold"),
        fg="#FFFFFF",
        bg="#2B394B"
    )
    account_label.pack(anchor="w", pady=(0, 8))

    account_entry = tk.Entry(
        account_card,
        font=("Arial", 12),
        bg="#1E293B",
        fg="#FFFFFF",
        insertbackground="#FFFFFF",
        relief="flat"
    )
    account_entry.pack(fill="x", ipady=10)

    def confirm_closure():

        account_number = account_entry.get().strip()

        if not account_number:
            messagebox.showerror(
                "Missing Information",
                "Please enter your account number."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Account Closure",
            "Are you sure you want to close this bank account?"
        )

        if not confirm:
            return

        try:
            close_account(customer_id, account_number)

            messagebox.showinfo(
                "Account Closed",
                "Your bank account has been closed successfully."
            )

            close_window.destroy()

        except ValueError as e:
            messagebox.showerror("Closure Failed", str(e))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    close_button = tk.Button(
        account_card,
        text="Close Account",
        font=("Arial", 12, "bold"),
        bg="#DC2626",
        fg="#FFFFFF",
        activebackground="#B91C1C",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=25,
        pady=11,
        command=confirm_closure
    )
    close_button.pack(pady=(25, 5))

    cancel_button = tk.Button(
        close_window,
        text="Cancel",
        font=("Arial", 11, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=20,
        pady=9,
        command=close_window.destroy
    )
    cancel_button.pack(pady=15)


def show_account_details(customer_id):
    details_window = tk.Toplevel(root)
    details_window.title("Account Details")
    details_window.geometry("550x550")
    details_window.configure(bg="#202B3C")

    tk.Label(
        details_window,
        text="Account Details",
        font=("Arial", 22, "bold"),
        bg="#202B3C",
        fg="white"
    ).pack(pady=25)

    tk.Label(
        details_window,
        text="Enter Account Number",
        font=("Arial", 12),
        bg="#202B3C",
        fg="#A7F3D0"
    ).pack(pady=10)

    account_entry = tk.Entry(
        details_window,
        font=("Arial", 13),
        bg="#1E293B",
        fg="white",
        insertbackground="white",
        width=28
    )
    account_entry.pack(pady=10)

    details_frame = tk.Frame(
        details_window,
        bg="#2B394B",
        padx=25,
        pady=20
    )

    def search_account():
        account_number = account_entry.get().strip()

        if not account_number:
            messagebox.showerror(
                "Error",
                "Please enter an account number"
            )
            return

        try:
            account = view_account_details(
                customer_id,
                account_number
            )

            for widget in details_frame.winfo_children():
                widget.destroy()

            details_frame.pack(pady=20, padx=25, fill="x")

            details = [
                ("Account Holder", account[0]),
                ("Account Number", account[1]),
                ("Available Balance", f"Rs. {account[2] / 100:,.2f}"),
                ("Account Status", account[3]),
                ("Created On", account[4])
            ]

            for label, value in details:
                tk.Label(
                    details_frame,
                    text=label,
                    font=("Arial", 11, "bold"),
                    bg="#2B394B",
                    fg="#A7F3D0",
                    anchor="w"
                ).pack(fill="x", pady=(8, 2))

                tk.Label(
                    details_frame,
                    text=str(value),
                    font=("Arial", 12),
                    bg="#2B394B",
                    fg="white",
                    anchor="w"
                ).pack(fill="x", pady=(0, 5))

        except ValueError as e:
            messagebox.showerror("Error", str(e))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        details_window,
        text="View Details",
        font=("Arial", 12, "bold"),
        bg="#10B981",
        fg="white",
        width=20,
        command=search_account
    ).pack(pady=20)

    tk.Button(
        details_window,
        text="Close",
        font=("Arial", 11),
        bg="#334155",
        fg="white",
        width=15,
        command=details_window.destroy
    ).pack(pady=10)


def show_account_statement(customer_id):
    statement_window = tk.Toplevel(root)
    statement_window.title("Account Statement")
    statement_window.geometry("1050x750")
    statement_window.configure(bg="#202B3C")

    tk.Label(
        statement_window,
        text="Account Statement",
        font=("Arial", 23, "bold"),
        bg="#202B3C",
        fg="white"
    ).pack(pady=20)

    input_frame = tk.Frame(
        statement_window,
        bg="#2B394B",
        padx=20,
        pady=15
    )
    input_frame.pack(fill="x", padx=25, pady=10)

    def create_field(label, row, column):
        tk.Label(
            input_frame,
            text=label,
            font=("Arial", 11, "bold"),
            bg="#2B394B",
            fg="#A7F3D0"
        ).grid(row=row, column=column, sticky="w", padx=10, pady=5)

        entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#1E293B",
            fg="white",
            insertbackground="white",
            width=23
        )
        entry.grid(row=row + 1, column=column, padx=10, pady=5)

        return entry

    account_entry = create_field("Account Number", 0, 0)
    start_entry = create_field("Start Date (YYYY-MM-DD)", 0, 1)
    end_entry = create_field("End Date (YYYY-MM-DD)", 0, 2)

    result_frame = tk.Frame(
        statement_window,
        bg="#202B3C"
    )

    summary_frame = tk.Frame(
        result_frame,
        bg="#2B394B",
        padx=20,
        pady=15
    )

    transaction_frame = tk.Frame(
        result_frame,
        bg="#2B394B",
        padx=15,
        pady=15
    )

    def generate_statement():
        account_number = account_entry.get().strip()
        start_date = start_entry.get().strip()
        end_date = end_entry.get().strip()

        if not account_number or not start_date or not end_date:
            messagebox.showerror(
                "Error",
                "Please fill in all fields"
            )
            return

        try:
            statement = generate_account_statement(
                customer_id,
                account_number,
                start_date,
                end_date
            )

            for widget in summary_frame.winfo_children():
                widget.destroy()

            for widget in transaction_frame.winfo_children():
                widget.destroy()

            summary_frame.pack(fill="x", pady=(0, 15))
            transaction_frame.pack(fill="both", expand=True)

            tk.Label(
                summary_frame,
                text=f"Account: {statement['account_number']}",
                font=("Arial", 13, "bold"),
                bg="#2B394B",
                fg="white"
            ).pack(anchor="w", pady=5)

            tk.Label(
                summary_frame,
                text=f"Period: {statement['start_date']} to {statement['end_date']}",
                font=("Arial", 11),
                bg="#2B394B",
                fg="#A7F3D0"
            ).pack(anchor="w", pady=5)

            summary_items = [
                ("Opening Balance", statement["opening_balance"]),
                ("Total Deposits", statement["deposits"]),
                ("Total Withdrawals", statement["withdrawals"]),
                ("Transfer In", statement["transfer_in"]),
                ("Transfer Out", statement["transfer_out"]),
                ("Closing Balance", statement["closing_balance"])
            ]

            values_frame = tk.Frame(
                summary_frame,
                bg="#2B394B"
            )
            values_frame.pack(fill="x", pady=10)

            for index, (label, amount) in enumerate(summary_items):
                item_frame = tk.Frame(
                    values_frame,
                    bg="#1E293B",
                    padx=10,
                    pady=10
                )
                item_frame.grid(
                    row=index // 3,
                    column=index % 3,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

                tk.Label(
                    item_frame,
                    text=label,
                    font=("Arial", 10, "bold"),
                    bg="#1E293B",
                    fg="#A7F3D0"
                ).pack(anchor="w")

                tk.Label(
                    item_frame,
                    text=f"Rs. {amount / 100:,.2f}",
                    font=("Arial", 12, "bold"),
                    bg="#1E293B",
                    fg="white"
                ).pack(anchor="w", pady=5)

            for column in range(3):
                values_frame.grid_columnconfigure(
                    column,
                    weight=1
                )

            tk.Label(
                transaction_frame,
                text="Transaction Details",
                font=("Arial", 15, "bold"),
                bg="#2B394B",
                fg="white"
            ).pack(anchor="w", pady=(0, 10))

            columns = (
                "ID",
                "Type",
                "Amount",
                "Date & Time"
            )

            tree = ttk.Treeview(
                transaction_frame,
                columns=columns,
                show="headings",
                height=8
            )

            tree.heading("ID", text="ID")
            tree.heading("Type", text="Transaction Type")
            tree.heading("Amount", text="Amount")
            tree.heading("Date & Time", text="Date & Time")

            tree.column("ID", width=60, anchor="center")
            tree.column("Type", width=180, anchor="center")
            tree.column("Amount", width=150, anchor="center")
            tree.column("Date & Time", width=220, anchor="center")

            scrollbar = ttk.Scrollbar(
                transaction_frame,
                orient="vertical",
                command=tree.yview
            )
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            if statement["transactions"]:
                for transaction in statement["transactions"]:
                    tree.insert(
                        "",
                        "end",
                        values=(
                            transaction[0],
                            transaction[1],
                            f"Rs. {transaction[2] / 100:,.2f}",
                            transaction[3]
                        )
                    )
            else:
                tk.Label(
                    transaction_frame,
                    text="No transactions during this period",
                    font=("Arial", 11),
                    bg="#2B394B",
                    fg="#A7F3D0"
                ).pack(pady=10)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        input_frame,
        text="Generate Statement",
        font=("Arial", 11, "bold"),
        bg="#10B981",
        fg="white",
        command=generate_statement
    ).grid(
        row=2,
        column=0,
        columnspan=3,
        pady=15
    )

    result_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    tk.Button(
        statement_window,
        text="Close",
        font=("Arial", 11),
        bg="#334155",
        fg="white",
        width=15,
        command=statement_window.destroy
    ).pack(pady=12)


def show_change_password(customer_id):
    password_window = tk.Toplevel(root)
    password_window.title("Change Password")
    password_window.geometry("500x500")
    password_window.configure(bg="#202B3C")

    tk.Label(
        password_window,
        text="Change Password",
        font=("Arial", 22, "bold"),
        bg="#202B3C",
        fg="white"
    ).pack(pady=25)

    form_frame = tk.Frame(
        password_window,
        bg="#2B394B",
        padx=25,
        pady=20
    )
    form_frame.pack(padx=30, fill="x")

    def create_password_field(label):
        tk.Label(
            form_frame,
            text=label,
            font=("Arial", 11, "bold"),
            bg="#2B394B",
            fg="#A7F3D0"
        ).pack(anchor="w", pady=(10, 5))

        entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#1E293B",
            fg="white",
            insertbackground="white",
            show="*",
            width=32
        )
        entry.pack(fill="x", pady=(0, 8))

        return entry

    current_entry = create_password_field("Current Password")
    new_entry = create_password_field("New Password")
    confirm_entry = create_password_field("Confirm New Password")

    def save_password():
        current_password = current_entry.get()
        new_password = new_entry.get()
        confirmed_password = confirm_entry.get()

        try:
            change_password(
                customer_id,
                current_password,
                new_password,
                confirmed_password
            )

            messagebox.showinfo(
                "Success",
                "Your password has been changed successfully."
            )

            password_window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        password_window,
        text="Update Password",
        font=("Arial", 12, "bold"),
        bg="#10B981",
        fg="white",
        width=22,
        command=save_password
    ).pack(pady=20)

    tk.Button(
        password_window,
        text="Cancel",
        font=("Arial", 11),
        bg="#334155",
        fg="white",
        width=15,
        command=password_window.destroy
    ).pack()



def show_forget_password():
    reset_window = tk.Toplevel(root)
    reset_window.title("Forgot Password")
    reset_window.geometry("500x600")
    reset_window.configure(bg="#202B3C")

    state = {
        "verification_code": None,
        "attempts": 0,
        "verified": False
    }

    tk.Label(
        reset_window,
        text="Reset Your Password",
        font=("Arial", 22, "bold"),
        bg="#202B3C",
        fg="white"
    ).pack(pady=25)

    form_frame = tk.Frame(
        reset_window,
        bg="#2B394B",
        padx=25,
        pady=20
    )
    form_frame.pack(fill="x", padx=30)

    def create_field(label, show=None):
        tk.Label(
            form_frame,
            text=label,
            font=("Arial", 11, "bold"),
            bg="#2B394B",
            fg="#A7F3D0"
        ).pack(anchor="w", pady=(10, 5))

        entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#1E293B",
            fg="white",
            insertbackground="white",
            show=show,
            width=32
        )
        entry.pack(fill="x", pady=(0, 8))

        return entry

    email_entry = create_field("Registered Email")
    code_entry = create_field("Six-Digit Verification Code")
    new_password_entry = create_field("New Password", show="*")
    confirm_password_entry = create_field("Confirm New Password", show="*")

    def send_code():
        email = email_entry.get().strip()

        if not email:
            messagebox.showerror("Error", "Please enter your registered email")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM customers WHERE email = ?",
                (email,)
            )

            customer = cursor.fetchone()

            if not customer:
                messagebox.showerror("Error", "User not found")
                return

            state["verification_code"] = str(
                secrets.randbelow(900000) + 100000
            )

            state["attempts"] = 0
            state["verified"] = False

            messagebox.showinfo(
                "Verification Code",
                f"Your verification code is: {state['verification_code']}"
            )

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if 'conn' in locals():
                conn.close()

    def verify_code():
        if state["verification_code"] is None:
            messagebox.showerror(
                "Error",
                "Please generate a verification code first"
            )
            return

        if state["verified"]:
            messagebox.showinfo("Verified", "Your email is already verified")
            return

        code = code_entry.get().strip()

        if len(code) != 6 or not code.isdigit():
            messagebox.showerror(
                "Error",
                "Please enter a valid six-digit code"
            )
            return

        if code == state["verification_code"]:
            state["verified"] = True

            messagebox.showinfo(
                "Success",
                "Email verified successfully!"
            )
            return

        state["attempts"] += 1

        if state["attempts"] >= 3:
            state["verification_code"] = None

            messagebox.showerror(
                "Verification Failed",
                "Too many incorrect attempts. Generate a new code to try again."
            )
        else:
            messagebox.showerror(
                "Incorrect Code",
                f"Incorrect code. {3 - state['attempts']} attempts remaining."
            )

    def reset_password():
        if not state["verified"]:
            messagebox.showerror(
                "Error",
                "Please verify your email first"
            )
            return

        email = email_entry.get().strip()
        code = code_entry.get().strip()
        new_password = new_password_entry.get()
        confirmed_password = confirm_password_entry.get()

        try:
            forget_password(
                email,
                state["verification_code"],
                code,
                new_password,
                confirmed_password
            )

            messagebox.showinfo(
                "Success",
                "Your password has been reset successfully!"
            )

            reset_window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        form_frame,
        text="Generate Verification Code",
        font=("Arial", 11, "bold"),
        bg="#10B981",
        fg="white",
        command=send_code
    ).pack(fill="x", pady=10)

    tk.Button(
        form_frame,
        text="Verify Code",
        font=("Arial", 11, "bold"),
        bg="#10B981",
        fg="white",
        command=verify_code
    ).pack(fill="x", pady=5)

    tk.Button(
        form_frame,
        text="Reset Password",
        font=("Arial", 11, "bold"),
        bg="#475569",
        fg="white",
        command=reset_password
    ).pack(fill="x", pady=10)

    tk.Button(
        reset_window,
        text="Cancel",
        font=("Arial", 11),
        bg="#334155",
        fg="white",
        width=15,
        command=reset_window.destroy
    ).pack(pady=15)



def logout():
    confirm = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if confirm:
        dashboard_title.pack_forget()
        welcome_label.pack_forget()
        dashboard_container.pack_forget()

        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        heading.pack(pady=30)
        subtitle.pack()
        login_frame.pack(pady=40)






def show_dashboard(customer_id):
    global dashboard_title, welcome_label, dashboard_container

    heading.pack_forget()
    subtitle.pack_forget()
    login_frame.pack_forget()

    dashboard_title = tk.Label(
        root,
        text="Customer Dashboard",
        font=("Arial", 26, "bold"),
        fg="#F1F5F9",
        bg="#202B3C"
    )
    dashboard_title.pack(pady=(25, 5))

    welcome_label = tk.Label(
        root,
        text="Welcome to your banking dashboard!",
        font=("Arial", 14),
        fg="#A7F3D0",
        bg="#202B3C"
    )
    welcome_label.pack(pady=(0, 20))

    dashboard_container = tk.Frame(root, bg="#202B3C")
    dashboard_container.pack(fill="both", expand=True, padx=60, pady=10)

    dashboard_frame = tk.Frame(
        dashboard_container,
        bg="#202B3C"
    )
    dashboard_frame.pack(expand=True)

    left_frame = tk.Frame(dashboard_frame, bg="#202B3C")
    left_frame.grid(row=0, column=0, padx=20, sticky="n")

    right_frame = tk.Frame(dashboard_frame, bg="#202B3C")
    right_frame.grid(row=0, column=1, padx=20, sticky="n")

    buttons = [
        ("My Accounts", "#2B394B", lambda: show_accounts(customer_id)),
        ("Create New Account", "#10B981", lambda: show_create_account(customer_id)),
        ("Deposit Money", "#2B394B", lambda: show_deposit(customer_id)),
        ("Withdraw Money", "#2B394B", lambda: show_withdraw(customer_id)),
        ("Transfer Money", "#2B394B", lambda: show_transfer(customer_id)),
        ("Transaction History", "#2B394B", lambda: show_transaction_history(customer_id)),
        ("My Profile", "#10B981", lambda: show_my_profile(customer_id)),
        ("Edit Profile", "#2B394B", lambda: show_update_profile(customer_id)),
        ("Check Balance", "#2B394B", lambda: show_check_balance(customer_id)),
        ("Close Bank Account", "#B91C1C", lambda: show_close_account(customer_id)),
        ("Account Details", "#2B394B", lambda: show_account_details(customer_id)),
        ("Account Statement", "#10B981", lambda: show_account_statement(customer_id)),
        ("Change Password", "#475569", lambda: show_change_password(customer_id))
    ]

    for index, (button_text, button_color, button_command) in enumerate(buttons):
        parent_frame = left_frame if index < 7 else right_frame

        tk.Button(
            parent_frame,
            text=button_text,
            font=("Arial", 12, "bold"),
            bg=button_color,
            fg="#FFFFFF",
            activebackground=button_color,
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            width=30,
            pady=12,
            command=button_command
        ).pack(pady=7)

    logout_button = tk.Button(
        dashboard_container,
        text="Logout",
        font=("Arial", 12, "bold"),
        bg="#B91C1C",
        fg="#FFFFFF",
        activebackground="#991B1B",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=30,
        pady=12,
        command=logout
    )
    logout_button.pack(pady=15)


def logout_admin():
    confirm = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if confirm:
        admin_title.pack_forget()
        admin_welcome.pack_forget()
        admin_container.pack_forget()

        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        heading.pack(pady=30)
        subtitle.pack()
        login_frame.pack(pady=40)




def show_admin_dashboard(admin_id):
    global admin_title, admin_welcome, admin_container

    heading.pack_forget()
    subtitle.pack_forget()
    login_frame.pack_forget()

    admin_title = tk.Label(
        root,
        text="Admin Dashboard",
        font=("Arial", 26, "bold"),
        fg=TEXT,
        bg=BG
    )
    admin_title.pack(pady=(25, 5))

    admin_welcome = tk.Label(
        root,
        text="Bank Management Control Panel",
        font=("Arial", 14),
        fg=ACCENT,
        bg=BG
    )
    admin_welcome.pack(pady=(0, 20))

    admin_container = tk.Frame(root, bg=BG)
    admin_container.pack(fill="both", expand=True, padx=60, pady=10)

    admin_frame = tk.Frame(admin_container, bg=BG)
    admin_frame.pack(expand=True)

    left_frame = tk.Frame(admin_frame, bg=BG)
    left_frame.grid(row=0, column=0, padx=20, sticky="n")

    right_frame = tk.Frame(admin_frame, bg=BG)
    right_frame.grid(row=0, column=1, padx=20, sticky="n")

    admin_buttons = [
        ("View All Customers", CARD, lambda: show_admin_customers()),
        ("Search Customer", CARD, lambda: show_admin_search_customer()),
        ("Update Customer", CARD, lambda: show_admin_update_customer()),
        ("Delete Customer", DANGER, lambda: show_admin_delete_customer()),
        ("View All Bank Accounts", CARD, lambda: show_admin_accounts()),
        ("Search Bank Account", CARD, lambda: show_admin_search_account()),
        ("Close Bank Account", DANGER, lambda: show_admin_close_account()),
        ("Reactivate Bank Account", PRIMARY, lambda: show_admin_reactivate_account()),
        ("View Bank Statistics", PRIMARY, lambda: show_admin_statistics()),
        ("View All Transactions", CARD, lambda: show_admin_transactions()),
        ("Search Transaction", CARD, lambda: show_admin_search_transaction()),
        ("Filter Transactions", CARD, lambda: show_admin_filter_transactions()),
        ("Transaction History By Date", CARD, lambda: show_admin_date_history()),
        ("Transaction Summary By Date", PRIMARY, lambda: show_admin_transaction_summary()),
        ("Create New Admin", PRIMARY, lambda: show_create_admin())
    ]

    for index, (button_text, button_color, button_command) in enumerate(admin_buttons):
        parent_frame = left_frame if index < 8 else right_frame

        tk.Button(
            parent_frame,
            text=button_text,
            font=("Arial", 12, "bold"),
            bg=button_color,
            fg=TEXT,
            activebackground=PRIMARY,
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            width=30,
            pady=12,
            command=button_command
        ).pack(pady=7)

    logout_button = tk.Button(
        admin_container,
        text="Logout",
        font=("Arial", 12, "bold"),
        bg=DANGER,
        fg="#FFFFFF",
        activebackground="#991B1B",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        width=30,
        pady=12,
        command=logout_admin
    )
    logout_button.pack(pady=15)

    def show_admin_customers():
        try:
            customers = view_customers()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return

        window = tk.Toplevel(root)
        window.title("All Customers")
        window.geometry("1000x600")
        window.configure(bg=BG)

        title = tk.Label(
            window,
            text="Registered Customers",
            font=("Arial", 24, "bold"),
            bg=BG,
            fg=TEXT
        )
        title.pack(pady=(25, 5))

        count_label = tk.Label(
            window,
            text=f"Total Customers: {len(customers)}",
            font=("Arial", 12),
            bg=BG,
            fg=ACCENT
        )
        count_label.pack(pady=(0, 20))

        if not customers:
            tk.Label(
                window,
                text="No customers found.",
                font=("Arial", 14),
                bg=BG,
                fg=TEXT
            ).pack(pady=50)

        else:
            table_frame = tk.Frame(window, bg=BG)
            table_frame.pack(fill="both", expand=True, padx=35, pady=10)

            columns = ("ID", "Name", "Email", "Phone")

            customer_table = ttk.Treeview(
                table_frame,
                columns=columns,
                show="headings"
            )

            customer_table.heading("ID", text="Customer ID")
            customer_table.heading("Name", text="Full Name")
            customer_table.heading("Email", text="Email Address")
            customer_table.heading("Phone", text="Phone Number")

            customer_table.column("ID", width=100, anchor="center")
            customer_table.column("Name", width=220, anchor="center")
            customer_table.column("Email", width=350, anchor="center")
            customer_table.column("Phone", width=200, anchor="center")

            scrollbar = ttk.Scrollbar(
                table_frame,
                orient="vertical",
                command=customer_table.yview
            )

            customer_table.configure(yscrollcommand=scrollbar.set)

            customer_table.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for customer in customers:
                customer_table.insert(
                    "",
                    "end",
                    values=customer
                )

        close_button = tk.Button(
            window,
            text="Close",
            font=("Arial", 12, "bold"),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        )
        close_button.pack(pady=20)

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
            ''', (search_value, f"%{search_value}%", f"%{search_value}%"))

            customers = cursor.fetchall()

            return customers

        except sqlite3.Error:
            raise

        finally:
            conn.close()

    def show_admin_update_customer():
        window = tk.Toplevel(root)
        window.title("Update Customer")
        window.geometry("500x550")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Update Customer",
            font=("Arial", 23, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=20)

        form_frame = tk.Frame(window, bg=BG)
        form_frame.pack(pady=10)

        tk.Label(
            form_frame,
            text="Customer Email",
            font=("Arial", 12),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(10, 5))

        email_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=35,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        email_entry.pack()

        tk.Label(
            form_frame,
            text="Customer Password",
            font=("Arial", 12),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(15, 5))

        password_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=35,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            show="*"
        )
        password_entry.pack()

        tk.Label(
            form_frame,
            text="New Phone Number",
            font=("Arial", 12),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(15, 5))

        phone_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=35,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        phone_entry.pack()

        def save_changes():
            email = email_entry.get().strip()
            password = password_entry.get()
            new_phone = phone_entry.get().strip()

            if not email or not password or not new_phone:
                messagebox.showerror(
                    "Input Error",
                    "Please fill in all fields."
                )
                return

            try:
                update_customer(email, password, new_phone)

                messagebox.showinfo(
                    "Success",
                    "Customer phone number updated successfully."
                )

                window.destroy()

            except ValueError as e:
                messagebox.showerror("Update Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            window,
            text="Save Changes",
            font=("Arial", 12, "bold"),
            bg=PRIMARY,
            fg=TEXT,
            width=20,
            command=save_changes
        ).pack(pady=25)

        tk.Button(
            window,
            text="Cancel",
            font=("Arial", 11),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack()

    def show_admin_delete_customer():
        window = tk.Toplevel(root)
        window.title("Delete Customer")
        window.geometry("500x480")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Delete Customer",
            font=("Arial", 23, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=20)

        tk.Label(
            window,
            text="Enter the customer's email and password.",
            font=("Arial", 11),
            bg=BG,
            fg=ACCENT
        ).pack(pady=5)

        form_frame = tk.Frame(window, bg=BG)
        form_frame.pack(pady=15)

        tk.Label(
            form_frame,
            text="Customer Email",
            font=("Arial", 12),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(10, 5))

        email_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=35,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        email_entry.pack()

        tk.Label(
            form_frame,
            text="Customer Password",
            font=("Arial", 12),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(15, 5))

        password_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=35,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            show="*"
        )
        password_entry.pack()

        def delete():
            email = email_entry.get().strip()
            password = password_entry.get()

            if not email or not password:
                messagebox.showerror(
                    "Input Error",
                    "Please fill in all fields."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Deletion",
                "Are you sure you want to delete this customer?\n\n"
                "This action cannot be undone."
            )

            if not confirm:
                return

            try:
                delete_customer(email, password)

                messagebox.showinfo(
                    "Success",
                    "Customer deleted successfully."
                )

                window.destroy()

            except ValueError as e:
                messagebox.showerror("Deletion Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            window,
            text="Delete Customer",
            font=("Arial", 12, "bold"),
            bg=DANGER,
            fg=TEXT,
            width=20,
            command=delete
        ).pack(pady=20)

        tk.Button(
            window,
            text="Cancel",
            font=("Arial", 11),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack()

    def show_admin_accounts():
        window = tk.Toplevel(root)
        window.title("All Bank Accounts")
        window.geometry("1100x600")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="All Bank Accounts",
            font=("Arial", 24, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=20)

        result_frame = tk.Frame(window, bg=BG)
        result_frame.pack(fill="both", expand=True, padx=25, pady=15)

        columns = (
            "Customer Name",
            "Account Number",
            "Balance",
            "Status",
            "Created On"
        )

        tree = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings",
            height=17
        )

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center", width=180)

        tree.column("Customer Name", width=190)
        tree.column("Account Number", width=190)
        tree.column("Balance", width=130)
        tree.column("Status", width=130)
        tree.column("Created On", width=190)

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        try:
            accounts = admin_view_account()

            if not accounts:
                tk.Label(
                    window,
                    text="No bank accounts found.",
                    font=("Arial", 12),
                    bg=BG,
                    fg=ACCENT
                ).pack(pady=5)

            else:
                for acc in accounts:
                    tree.insert(
                        "",
                        "end",
                        values=(
                            acc[0],
                            acc[1],
                            f"Rs. {float(acc[2]) / 100:,.2f}",
                            acc[3],
                            acc[4]
                        )
                    )

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            window.destroy()
            return

        tk.Button(
            window,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack(pady=15)

    def show_admin_search_account():
        window = tk.Toplevel(root)
        window.title("Search Bank Account")
        window.geometry("750x480")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Search Bank Account",
            font=("Arial", 23, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=20)

        search_frame = tk.Frame(window, bg=BG)
        search_frame.pack(pady=15)

        tk.Label(
            search_frame,
            text="Account Number",
            font=("Arial", 12),
            bg=BG,
            fg=TEXT
        ).pack(pady=5)

        account_entry = tk.Entry(
            search_frame,
            font=("Arial", 13),
            width=35,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        account_entry.pack(pady=5)

        result_frame = tk.Frame(window, bg=BG)
        result_frame.pack(fill="both", expand=True, padx=25, pady=20)

        columns = (
            "Customer Name",
            "Account Number",
            "Balance",
            "Status",
            "Created On"
        )

        tree = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings",
            height=5
        )

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center", width=140)

        tree.column("Customer Name", width=150)
        tree.column("Account Number", width=150)
        tree.column("Balance", width=110)
        tree.column("Status", width=100)
        tree.column("Created On", width=170)

        tree.pack(fill="x", expand=True)

        def search():
            account_number = account_entry.get().strip()

            if not account_number:
                messagebox.showerror(
                    "Input Error",
                    "Please enter an account number."
                )
                return

            for item in tree.get_children():
                tree.delete(item)

            try:
                account = admin_search_account(account_number)

                if not account:
                    messagebox.showinfo(
                        "Not Found",
                        "Bank account not found."
                    )
                    return

                tree.insert(
                    "",
                    "end",
                    values=(
                        account[0],
                        account[1],
                        f"Rs. {float(account[2]) / 100:,.2f}",
                        account[3],
                        account[4]
                    )
                )

            except ValueError as e:
                messagebox.showerror("Search Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 12, "bold"),
            bg=PRIMARY,
            fg=TEXT,
            width=18,
            command=search
        ).pack(pady=15)

        tk.Button(
            window,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack(pady=15)

    def show_admin_close_account():
        window = tk.Toplevel(root)
        window.title("Close Bank Account")
        window.geometry("500x400")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Close Bank Account",
            font=("Arial", 23, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=25)

        tk.Label(
            window,
            text="Enter the account number you want to close.",
            font=("Arial", 11),
            bg=BG,
            fg=ACCENT
        ).pack(pady=10)

        account_entry = tk.Entry(
            window,
            font=("Arial", 13),
            width=32,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        account_entry.pack(pady=15)

        def close_account():
            account_number = account_entry.get().strip()

            if not account_number:
                messagebox.showerror(
                    "Input Error",
                    "Please enter an account number."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Account Closure",
                f"Are you sure you want to close account {account_number}?"
            )

            if not confirm:
                return

            try:
                admin_close_account(account_number)

                messagebox.showinfo(
                    "Success",
                    "Bank account has been closed successfully."
                )

                window.destroy()

            except ValueError as e:
                messagebox.showerror("Closure Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            window,
            text="Close Account",
            font=("Arial", 12, "bold"),
            bg=DANGER,
            fg=TEXT,
            width=20,
            command=close_account
        ).pack(pady=20)

        tk.Button(
            window,
            text="Cancel",
            font=("Arial", 11),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack()

    def show_admin_reactivate_account():
        window = tk.Toplevel(root)
        window.title("Reactivate Bank Account")
        window.geometry("500x400")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Reactivate Bank Account",
            font=("Arial", 22, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=25)

        tk.Label(
            window,
            text="Enter the account number you want to reactivate.",
            font=("Arial", 11),
            bg=BG,
            fg=ACCENT
        ).pack(pady=10)

        account_entry = tk.Entry(
            window,
            font=("Arial", 13),
            width=32,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        account_entry.pack(pady=15)

        def reactivate():
            account_number = account_entry.get().strip()

            if not account_number:
                messagebox.showerror(
                    "Input Error",
                    "Please enter an account number."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Reactivation",
                f"Are you sure you want to reactivate account {account_number}?"
            )

            if not confirm:
                return

            try:
                admin_reactivate_account(account_number)

                messagebox.showinfo(
                    "Success",
                    "Bank account has been reactivated successfully."
                )

                window.destroy()

            except ValueError as e:
                messagebox.showerror("Reactivation Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            window,
            text="Reactivate Account",
            font=("Arial", 12, "bold"),
            bg=PRIMARY,
            fg=TEXT,
            width=22,
            command=reactivate
        ).pack(pady=20)

        tk.Button(
            window,
            text="Cancel",
            font=("Arial", 11),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack()

    def show_admin_statistics():
        window = tk.Toplevel(root)
        window.title("Bank Statistics")
        window.geometry("1000x700")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Bank Statistics",
            font=("Arial", 26, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(25, 5))

        tk.Label(
            window,
            text="Overview of your bank's performance",
            font=("Arial", 12),
            bg=BG,
            fg=ACCENT
        ).pack(pady=(0, 25))

        try:
            stats = admin_dashboard_stats()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            window.destroy()
            return

        cards = [
            ("Total Customers", stats["total_customers"], "👥"),
            ("Total Accounts", stats["total_accounts"], "🏦"),
            ("Active Accounts", stats["active_accounts"], "✓"),
            ("Closed Accounts", stats["closed_accounts"], "×"),
            ("Total Deposits", f"Rs. {float(stats['total_deposits']) / 100:,.2f}", "+"),
            ("Total Withdrawals", f"Rs. {float(stats['total_withdrawals']) / 100:,.2f}", "−"),
            ("Transfers Out", f"Rs. {float(stats['total_transfer_out']) / 100:,.2f}", "↗"),
            ("Transfers In", f"Rs. {float(stats['total_transfer_in']) / 100:,.2f}", "↙"),
            ("Total Bank Balance", f"Rs. {float(stats['total_balance']) / 100:,.2f}", "Rs.")
        ]

        cards_frame = tk.Frame(window, bg=BG)
        cards_frame.pack(fill="both", expand=True, padx=35, pady=10)

        for index, (title, value, symbol) in enumerate(cards):
            row = index // 3
            column = index % 3

            card = tk.Frame(
                cards_frame,
                bg=CARD,
                highlightbackground=SECONDARY,
                highlightthickness=1
            )

            card.grid(
                row=row,
                column=column,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=symbol,
                font=("Arial", 20, "bold"),
                bg=CARD,
                fg=ACCENT
            ).pack(pady=(18, 5))

            tk.Label(
                card,
                text=title,
                font=("Arial", 12, "bold"),
                bg=CARD,
                fg=TEXT
            ).pack(pady=5)

            tk.Label(
                card,
                text=value,
                font=("Arial", 17, "bold"),
                bg=CARD,
                fg=PRIMARY
            ).pack(pady=(5, 20))

        for column in range(3):
            cards_frame.grid_columnconfigure(column, weight=1)

        for row in range(3):
            cards_frame.grid_rowconfigure(row, weight=1)

        tk.Button(
            window,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack(pady=20)

    def show_admin_transactions():
        window = tk.Toplevel(root)
        window.title("All Transactions")
        window.geometry("1150x650")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="All Transactions",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(20, 5))

        tk.Label(
            window,
            text="Complete bank transaction history",
            font=("Arial", 12),
            bg=BG,
            fg=ACCENT
        ).pack(pady=(0, 20))

        result_frame = tk.Frame(window, bg=BG)
        result_frame.pack(fill="both", expand=True, padx=25, pady=10)

        columns = (
            "ID",
            "Customer Name",
            "Account Number",
            "Transaction Type",
            "Amount",
            "Timestamp"
        )

        tree = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings",
            height=20
        )

        widths = {
            "ID": 55,
            "Customer Name": 190,
            "Account Number": 175,
            "Transaction Type": 170,
            "Amount": 140,
            "Timestamp": 190
        }

        for column in columns:
            tree.heading(column, text=column)
            tree.column(
                column,
                anchor="center",
                width=widths[column]
            )

        vertical_scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            result_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        try:
            transactions = admin_view_transactions()

            if not transactions:
                tk.Label(
                    window,
                    text="No transactions found.",
                    font=("Arial", 12),
                    bg=BG,
                    fg=ACCENT
                ).pack(pady=5)

            else:
                for tran in transactions:
                    tree.insert(
                        "",
                        "end",
                        values=(
                            tran[0],
                            tran[1],
                            tran[2],
                            tran[3],
                            f"Rs. {float(tran[4]) / 100:,.2f}",
                            tran[5]
                        )
                    )

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            window.destroy()
            return

        tk.Button(
            window,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack(pady=15)

    def show_admin_search_transaction():
        window = tk.Toplevel(root)
        window.title("Search Transaction")
        window.geometry("650x600")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Search Transaction",
            font=("Arial", 24, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(25, 10))

        tk.Label(
            window,
            text="Enter Transaction ID",
            font=("Arial", 12),
            bg=BG,
            fg=ACCENT
        ).pack(pady=10)

        transaction_entry = tk.Entry(
            window,
            font=("Arial", 13),
            width=30,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        transaction_entry.pack(pady=5)

        result_frame = tk.Frame(window, bg=CARD)
        result_frame.pack(fill="both", expand=True, padx=45, pady=25)

        result_labels = {}

        fields = [
            "Transaction ID",
            "Customer Name",
            "Customer ID",
            "Account Number",
            "Transaction Type",
            "Amount",
            "Timestamp"
        ]

        for field in fields:
            row = tk.Frame(result_frame, bg=CARD)
            row.pack(fill="x", padx=15, pady=9)

            tk.Label(
                row,
                text=field + ":",
                font=("Arial", 11, "bold"),
                bg=CARD,
                fg=ACCENT,
                width=18,
                anchor="w"
            ).pack(side="left")

            value_label = tk.Label(
                row,
                text="—",
                font=("Arial", 11),
                bg=CARD,
                fg=TEXT,
                anchor="w"
            )
            value_label.pack(side="left", fill="x", expand=True)

            result_labels[field] = value_label

        def search():
            transaction_id = transaction_entry.get().strip()

            if not transaction_id:
                messagebox.showerror(
                    "Input Error",
                    "Please enter a transaction ID."
                )
                return

            for label in result_labels.values():
                label.config(text="—")

            try:
                transaction = admin_search_transaction(transaction_id)

                if not transaction:
                    messagebox.showinfo(
                        "Not Found",
                        "No transaction found with this ID."
                    )
                    return

                values = [
                    transaction[0],
                    transaction[1],
                    transaction[2],
                    transaction[3],
                    transaction[4],
                    f"Rs. {float(transaction[5]) / 100:,.2f}",
                    transaction[6]
                ]

                for field, value in zip(fields, values):
                    result_labels[field].config(text=str(value))

            except ValueError as e:
                messagebox.showerror("Search Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            window,
            text="Search",
            font=("Arial", 12, "bold"),
            bg=PRIMARY,
            fg=TEXT,
            width=18,
            command=search
        ).pack(pady=5)

        tk.Button(
            window,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack(pady=15)

    def show_admin_filter_transactions():
        window = tk.Toplevel(root)
        window.title("Filter Transactions")
        window.geometry("1150x650")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Filter Transactions",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(20, 5))

        tk.Label(
            window,
            text="Select a transaction type to view matching records",
            font=("Arial", 12),
            bg=BG,
            fg=ACCENT
        ).pack(pady=(0, 15))

        filter_frame = tk.Frame(window, bg=BG)
        filter_frame.pack(pady=10)

        tk.Label(
            filter_frame,
            text="Transaction Type",
            font=("Arial", 12),
            bg=BG,
            fg=TEXT
        ).pack(side="left", padx=10)

        transaction_type = tk.StringVar(value="All Transactions")

        transaction_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=transaction_type,
            values=[
                "All Transactions",
                "Deposit",
                "Withdraw",
                "Transfer In",
                "Transfer Out"
            ],
            state="readonly",
            font=("Arial", 11),
            width=22
        )
        transaction_dropdown.pack(side="left", padx=10)

        result_frame = tk.Frame(window, bg=BG)
        result_frame.pack(fill="both", expand=True, padx=25, pady=15)

        columns = (
            "ID",
            "Customer Name",
            "Account Number",
            "Transaction Type",
            "Amount",
            "Timestamp"
        )

        tree = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings",
            height=17
        )

        widths = {
            "ID": 55,
            "Customer Name": 190,
            "Account Number": 175,
            "Transaction Type": 170,
            "Amount": 140,
            "Timestamp": 190
        }

        for column in columns:
            tree.heading(column, text=column)
            tree.column(
                column,
                anchor="center",
                width=widths[column]
            )

        vertical_scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            result_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        def filter_transactions():
            for item in tree.get_children():
                tree.delete(item)

            selected_type = transaction_type.get()

            try:
                transactions = admin_filter_transactions(selected_type)

                if not transactions:
                    messagebox.showinfo(
                        "No Results",
                        f"No {selected_type.lower()} found."
                    )
                    return

                for tran in transactions:
                    tree.insert(
                        "",
                        "end",
                        values=(
                            tran[0],
                            tran[1],
                            tran[2],
                            tran[3],
                            f"Rs. {float(tran[4]) / 100:,.2f}",
                            tran[5]
                        )
                    )

            except ValueError as e:
                messagebox.showerror("Filter Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            filter_frame,
            text="Apply Filter",
            font=("Arial", 11, "bold"),
            bg=PRIMARY,
            fg=TEXT,
            command=filter_transactions
        ).pack(side="left", padx=10)

        tk.Button(
            window,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack(pady=15)

        filter_transactions()

    def show_admin_date_history():
        window = tk.Toplevel(root)
        window.title("Transaction History By Date")
        window.geometry("1150x680")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Transaction History By Date",
            font=("Arial", 24, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(20, 5))

        tk.Label(
            window,
            text="View transactions within a selected date range",
            font=("Arial", 12),
            bg=BG,
            fg=ACCENT
        ).pack(pady=(0, 15))

        filter_frame = tk.Frame(window, bg=BG)
        filter_frame.pack(pady=15)

        tk.Label(
            filter_frame,
            text="Start Date (YYYY-MM-DD)",
            font=("Arial", 11),
            bg=BG,
            fg=TEXT
        ).grid(row=0, column=0, padx=12, pady=5)

        tk.Label(
            filter_frame,
            text="End Date (YYYY-MM-DD)",
            font=("Arial", 11),
            bg=BG,
            fg=TEXT
        ).grid(row=0, column=1, padx=12, pady=5)

        start_entry = tk.Entry(
            filter_frame,
            font=("Arial", 12),
            width=22,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        start_entry.grid(row=1, column=0, padx=12, pady=5)

        end_entry = tk.Entry(
            filter_frame,
            font=("Arial", 12),
            width=22,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        end_entry.grid(row=1, column=1, padx=12, pady=5)

        result_frame = tk.Frame(window, bg=BG)
        result_frame.pack(fill="both", expand=True, padx=25, pady=15)

        columns = (
            "ID",
            "Customer Name",
            "Account Number",
            "Transaction Type",
            "Amount",
            "Timestamp"
        )

        tree = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings",
            height=17
        )

        widths = {
            "ID": 55,
            "Customer Name": 190,
            "Account Number": 175,
            "Transaction Type": 170,
            "Amount": 140,
            "Timestamp": 190
        }

        for column in columns:
            tree.heading(column, text=column)
            tree.column(
                column,
                anchor="center",
                width=widths[column]
            )

        vertical_scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            result_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        def search_by_date():
            start_date = start_entry.get().strip()
            end_date = end_entry.get().strip()

            for item in tree.get_children():
                tree.delete(item)

            try:
                transactions = admin_filter_transaction_by_date(
                    start_date,
                    end_date
                )

                if not transactions:
                    messagebox.showinfo(
                        "No Results",
                        "No transactions found within these dates."
                    )
                    return

                for tran in transactions:
                    tree.insert(
                        "",
                        "end",
                        values=(
                            tran[0],
                            tran[1],
                            tran[2],
                            tran[3],
                            f"Rs. {float(tran[4]) / 100:,.2f}",
                            tran[5]
                        )
                    )

            except ValueError as e:
                messagebox.showerror("Date Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            filter_frame,
            text="Search Transactions",
            font=("Arial", 11, "bold"),
            bg=PRIMARY,
            fg=TEXT,
            command=search_by_date
        ).grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(
            window,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack(pady=15)

    def show_admin_transaction_summary():
        window = tk.Toplevel(root)
        window.title("Transaction Summary")
        window.geometry("750x700")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Transaction Summary",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(25, 5))

        tk.Label(
            window,
            text="Analyze bank transactions within a date range",
            font=("Arial", 12),
            bg=BG,
            fg=ACCENT
        ).pack(pady=(0, 20))

        filter_frame = tk.Frame(window, bg=BG)
        filter_frame.pack(pady=10)

        tk.Label(
            filter_frame,
            text="Start Date (YYYY-MM-DD)",
            font=("Arial", 11),
            bg=BG,
            fg=TEXT
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Label(
            filter_frame,
            text="End Date (YYYY-MM-DD)",
            font=("Arial", 11),
            bg=BG,
            fg=TEXT
        ).grid(row=0, column=1, padx=10, pady=5)

        start_entry = tk.Entry(
            filter_frame,
            font=("Arial", 12),
            width=22,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        start_entry.grid(row=1, column=0, padx=10, pady=5)

        end_entry = tk.Entry(
            filter_frame,
            font=("Arial", 12),
            width=22,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        end_entry.grid(row=1, column=1, padx=10, pady=5)

        result_frame = tk.Frame(window, bg=BG)
        result_frame.pack(fill="both", expand=True, padx=35, pady=20)

        result_title = tk.Label(
            result_frame,
            text="Select a date range to view the summary",
            font=("Arial", 12),
            bg=BG,
            fg=ACCENT
        )
        result_title.pack(pady=10)

        summary_labels = {}

        summary_items = [
            ("Total Transactions", "total_transactions", False),
            ("Total Deposits", "total_deposits", True),
            ("Total Withdrawals", "total_withdrawals", True),
            ("Total Transfer In", "total_transfer_in", True),
            ("Total Transfer Out", "total_transfer_out", True)
        ]

        for title, key, is_amount in summary_items:
            card = tk.Frame(
                result_frame,
                bg=CARD,
                highlightbackground=SECONDARY,
                highlightthickness=1
            )
            card.pack(fill="x", pady=6)

            tk.Label(
                card,
                text=title,
                font=("Arial", 11, "bold"),
                bg=CARD,
                fg=ACCENT
            ).pack(side="left", padx=20, pady=15)

            value_label = tk.Label(
                card,
                text="—",
                font=("Arial", 13, "bold"),
                bg=CARD,
                fg=TEXT
            )
            value_label.pack(side="right", padx=20, pady=15)

            summary_labels[key] = (value_label, is_amount)

        def generate_summary():
            start_date = start_entry.get().strip()
            end_date = end_entry.get().strip()

            try:
                summary = admin_transaction_summary(
                    start_date,
                    end_date
                )

                result_title.config(
                    text=f"{summary['start_date']}  to  {summary['end_date']}"
                )

                for title, key, is_amount in summary_items:
                    value = summary[key]

                    if is_amount:
                        value = f"Rs. {float(value) / 100:,.2f}"

                    summary_labels[key][0].config(text=str(value))

            except ValueError as e:
                messagebox.showerror("Date Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            filter_frame,
            text="Generate Summary",
            font=("Arial", 11, "bold"),
            bg=PRIMARY,
            fg=TEXT,
            command=generate_summary
        ).grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(
            window,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=SECONDARY,
            fg=TEXT,
            width=15,
            command=window.destroy
        ).pack(pady=15)

    def show_create_admin():
        window = tk.Toplevel(root)
        window.title("Create New Admin")
        window.geometry("500x570")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="Create New Admin",
            font=("Arial", 24, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(30, 8))

        tk.Label(
            window,
            text="Add a new administrator to the banking system",
            font=("Arial", 11),
            bg=BG,
            fg=ACCENT
        ).pack(pady=(0, 25))

        form_frame = tk.Frame(window, bg=BG)
        form_frame.pack(fill="x", padx=55)

        tk.Label(
            form_frame,
            text="Admin Username",
            font=("Arial", 11, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(5, 7))

        username_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        username_entry.pack(fill="x", ipady=8, pady=(0, 15))

        tk.Label(
            form_frame,
            text="Password",
            font=("Arial", 11, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(5, 7))

        password_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            show="*",
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        password_entry.pack(fill="x", ipady=8, pady=(0, 15))

        tk.Label(
            form_frame,
            text="Confirm Password",
            font=("Arial", 11, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(5, 7))

        confirm_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            show="*",
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT
        )
        confirm_entry.pack(fill="x", ipady=8, pady=(0, 20))

        def create_admin():
            username = username_entry.get().strip()
            password = password_entry.get()
            confirm_password = confirm_entry.get()

            try:
                add_admin(
                    username,
                    password,
                    confirm_password
                )

                messagebox.showinfo(
                    "Success",
                    "New admin account created successfully!"
                )

                window.destroy()

            except ValueError as e:
                messagebox.showerror("Validation Error", str(e))

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            window,
            text="Create Admin Account",
            font=("Arial", 12, "bold"),
            bg=PRIMARY,
            fg=TEXT,
            width=25,
            command=create_admin
        ).pack(pady=10)

        tk.Button(
            window,
            text="Cancel",
            font=("Arial", 11),
            bg=SECONDARY,
            fg=TEXT,
            width=20,
            command=window.destroy
        ).pack(pady=8)




def login():
    email = email_entry.get().strip()
    password = password_entry.get()

    if email == email_placeholder or not email:
        messagebox.showerror(
            "Login Error",
            "Please enter your email address or admin username."
        )
        return

    if password == "Enter your password" or not password:
        messagebox.showerror("Login Error", "Please enter your password.")
        return

    try:
        customer_id = login_customer(email, password)

        if customer_id is not None:
            messagebox.showinfo(
                "Login Successful",
                "Welcome back! You have logged in successfully."
            )
            show_dashboard(customer_id)
            return

        admin_id = login_admin(email, password)

        if admin_id is not None:
            messagebox.showinfo(
                "Login Successful",
                "Welcome back, Admin!"
            )
            show_admin_dashboard(admin_id)
            return

        messagebox.showerror(
            "Login Failed",
            "Invalid email/username or password."
        )

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


login_button = tk.Button(
    login_frame,
    text="Login",
    font=("Arial", 12, "bold"),
    bg="#10B981",
    fg = "#FFFFFF",
    activebackground="#1D4ED8",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    width = 30,
    pady=10,
    command=login
)
login_button.pack(pady=25)

forgot_button = tk.Button(
    login_frame,
    text="Forgot Password?",
    font=("Arial", 10, "underline"),
    bg="#202B3C",
    fg="#A7F3D0",
    activebackground="#202B3C",
    activeforeground="white",
    relief="flat",
    command=show_forget_password
)
forgot_button.pack(pady=10)

register_label = tk.Label(
    login_frame,
    text="Dont have an account? Register",
    font=("Arial", 10),
    fg = "#60A5FA",
    bg="#2B394B",
    cursor="hand2",
)
register_label.pack()

register_label.bind(
    "<Button-1>",
    lambda event: print("Register clicked!")
)

def show_admin_search_customer():
    window = tk.Toplevel(root)
    window.title("Search Customer")
    window.geometry("850x550")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="Search Customer",
        font=("Arial", 24, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=(20, 5))

    tk.Label(
        window,
        text="Search using Customer ID, Name or Email",
        font=("Arial", 12),
        bg=BG,
        fg=ACCENT
    ).pack(pady=(0, 15))

    search_frame = tk.Frame(window, bg=BG)
    search_frame.pack(pady=10)

    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 12),
        width=40,
        bg=CARD,
        fg=TEXT,
        insertbackground=TEXT
    )
    search_entry.pack(pady=10)

    result_frame = tk.Frame(window, bg=BG)
    result_frame.pack(fill="both", expand=True, padx=25, pady=15)

    columns = ("ID", "Name", "Email", "Phone")

    tree = ttk.Treeview(
        result_frame,
        columns=columns,
        show="headings",
        height=12
    )

    widths = {
        "ID": 70,
        "Name": 200,
        "Email": 280,
        "Phone": 170
    }

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, anchor="center", width=widths[column])

    scrollbar = ttk.Scrollbar(
        result_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def search():
        search_value = search_entry.get().strip()

        for item in tree.get_children():
            tree.delete(item)

        if not search_value:
            messagebox.showerror(
                "Search Error",
                "Please enter a customer ID, name or email."
            )
            return

        try:
            customers = search_customer(search_value)

            if not customers:
                messagebox.showinfo(
                    "No Results",
                    "No matching customer found."
                )
                return

            for customer in customers:
                tree.insert("", "end", values=customer)

        except ValueError as e:
            messagebox.showerror("Search Error", str(e))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        search_frame,
        text="Search Customer",
        font=("Arial", 11, "bold"),
        bg=PRIMARY,
        fg=TEXT,
        width=20,
        command=search
    ).pack(pady=5)

    tk.Button(
        window,
        text="Close",
        font=("Arial", 11, "bold"),
        bg=SECONDARY,
        fg=TEXT,
        width=15,
        command=window.destroy
    ).pack(pady=15)

root.mainloop()