from database import create_table
from bank import register_customer, view_customers, search_customer, update_customer, login_customer, login_admin, delete_customer, change_password, forget_password, view_my_profile, update_profile, add_admin
from account import create_account, view_my_accounts, check_balance, generate_account_statement, deposit_money, withdraw_money, transfer_money, view_transaction_history, close_account, view_account_details, admin_view_account, admin_search_account, admin_close_account, admin_reactivate_account, admin_dashboard_stats, admin_view_transactions,admin_search_transaction,admin_filter_transactions, admin_filter_transaction_by_date, admin_transaction_summary

create_table()

print("Database connected successfully")

while True:
    customer_id = None
    admin_id = None
    print("\n================================ BANKING MANAGEMENT SYSTEM ================================\n")
    print("1. Register")
    print("2. Login")
    print("3. Admin Login")
    print("4. Forget Password")
    print("5. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a valid choice")
        continue
    if choice == 1:
        customer_id = register_customer()
    elif choice == 2:
        customer_id = login_customer()
    elif choice == 3:
        admin_id = login_admin()
    elif choice == 4:
        forget_password()
    elif choice == 5:
        break
    else:
        print("Please enter a valid choice")
        continue

    if customer_id is not None:
        while True:
            print("\n\n================================ CUSTOMER DASHBOARD ================================\n")
            print("1. View My Accounts\n2. Create Bank Account\n3. Check Balance\n4. Deposit Money\n5. Withdraw Money\n6. Transfer Money\n7. Transaction History\n8. Close Account\n9. View Account Details\n10. Generate Account Statement\n11. Change Password\n12. View My Profile\n13. Update Profile\n14. Logout")
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    print("========== MY ACCOUNTS ==========")
                    view_my_accounts(customer_id)
                elif choice == 2:
                    print("========== CREATE ACCOUNT ============")
                    create_account(customer_id)
                elif choice == 3:
                    print("==========BALANCE==========")
                    check_balance(customer_id)
                elif choice == 4:
                    print("========== DEPOSIT MONEY ==========")
                    deposit_money(customer_id)
                elif choice == 5:
                    print("========== WITHDRAW MONEY ==========")
                    withdraw_money(customer_id)
                elif choice == 6:
                    print("========== TRANSFER MONEY ==========")
                    transfer_money(customer_id)
                elif choice == 7:
                    print("========== TRANSACTION HISTORY ==========")
                    view_transaction_history(customer_id)
                elif choice == 8:
                    print("========== CLOSE ACCOUNT ==========")
                    close_account(customer_id)
                elif choice == 9:
                    print("========== ACCOUNT DETAILS ==========")
                    view_account_details(customer_id)
                elif choice == 10:
                    generate_account_statement(customer_id)
                elif choice == 11:
                    print("========== CHANGE PASSWORD ==========")
                    change_password(customer_id)
                elif choice == 12:
                    print("========== MY PROFILE ==========")
                    view_my_profile(customer_id)
                elif choice == 13:
                    print("========== UPDATE PROFILE ==========")
                    update_profile(customer_id)
                elif choice == 14:
                    break
                else:
                    print("Please enter a valid choice")
            except ValueError:
                print("Please enter a valid choice")

    if admin_id is not None:
        while True:
            print("\n============================== ADMIN DASHBOARD ==============================\n")
            print("1. View All Customers")
            print("2. Search Customer")
            print("3. Update Customer")
            print("4. Delete Customer")
            print("5. View All Bank Accounts")
            print("6. Search Bank Account")
            print("7. Close Bank Account")
            print("8. Reactivate Bank Account")
            print("9. View Bank Statistics")
            print("10. View All Transactions")
            print("11. Search Transaction")
            print("12. Search Transaction By Filter")
            print("13. Search Transaction History By Date")
            print("14. Transaction Summary By Date")
            print("15. Create New Admin Account")
            print("16. Logout")
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    print("========== CUSTOMERS ==========")
                    view_customers()
                elif choice == 2:
                    print("========== SEARCH CUSTOMERS ==========")
                    search_customer()
                elif choice == 3:
                    print("========== UPDATE CUSTOMERS ==========")
                    update_customer()
                elif choice == 4:
                    print("========== DELETE CUSTOMERS ==========")
                    delete_customer()
                elif choice == 5:
                    print("========== VIEW BANK ACCOUNTS ==========")
                    admin_view_account()
                elif choice == 6:
                    print("========== SEARCH BANK ACCOUNTS ==========")
                    admin_search_account()
                elif choice == 7:
                    print("========== CLOSE BANK ACCOUNTS ==========")
                    admin_close_account()
                elif choice == 8:
                    print("========== RE-ACTIVE BANK ACCOUNT ==========")
                    admin_reactivate_account()
                elif choice == 9:
                    print("========== VIEW BANK STATISTICS ==========")
                    admin_dashboard_stats()
                elif choice == 10:
                    print("========== VIEW TRANSACTION HISTORY ==========")
                    admin_view_transactions()
                elif choice == 11:
                    print("========== SEARCH TRANSACTIONS ==========")
                    admin_search_transaction()
                elif choice == 12:
                    print("========== FILTER TRANSACTIONS ==========")
                    admin_filter_transactions()
                elif choice == 13:
                    print("========== TRANSACTION HISTORY BY DATE ==========")
                    admin_filter_transaction_by_date()
                elif choice == 14:
                    print("========== TRANSACTION SUMMARY BY DATE ==========")
                    admin_transaction_summary()
                elif choice == 15:
                    print("========== CREATE ADMIN ACCOUNT ==========")
                    add_admin()
                elif choice == 16:
                    break
                else:
                    print("Please enter a valid choice")
            except ValueError:
                print("Please enter a valid choice")
    elif customer_id is None and admin_id is None:
        print("Unable to proceed. Please try again")
