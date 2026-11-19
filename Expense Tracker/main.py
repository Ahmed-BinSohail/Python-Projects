# Expense Tracker - add, view, search and save expenses

import json

print("Expense Tracker Started")

expenses = []

def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file)
        print("Expense saved successfully!")

def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)
            expenses.extend(data)
            print("Expenses loaded!")
    except FileNotFoundError:
        print("No expenses saved!")


def add_expense():
    ex_name = input("Enter expense name: ").strip()
    if ex_name == "":
        print("Expense name cannot be empty!")
        return
    try:
        ex_amount = float(input("Enter expense amount: "))
    except ValueError:
        print("Please enter a valid amount!")
        return
    ex_category = input("Enter expense category: ").upper().strip()
    if ex_category == "":
        print("Expense category cannot be empty!")
        return
    expense = {"name": ex_name, "amount": ex_amount, "category": ex_category}
    expenses.append(expense)
    print("Expense added successfully!")

def view_expenses():
    if expenses == []:
        print("Expense list is empty!")
    else:
        for expense in expenses:
            print(f'Name: {expense["name"]}\nAmount: {expense["amount"]}\nCategory: {expense["category"]}')

def calculate_total():
    total = 0
    for expense in expenses:
        total += expense["amount"]
    print(f"Total expenses: {total}")

def search_expenses():
    category = input("Enter expense category: ").upper()
    found = False
    for expense in expenses:
        if expense["category"] == category:
            print(f"Name: {expense['name']}\nAmount: {expense['amount']}")
            found = True
    if not found:
            print("Expense not found!")

def main_menu():
    while True:
        print("\n1. Add new expense\n2. View expenses\n3. Caclulate total\n4. Search expenses\n5. Save expenses\n6. Exit\n")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid choice!")
            continue
        if choice == 1:
            add_expense()
        elif choice == 2:
            view_expenses()
        elif choice == 3:
            calculate_total()
        elif choice == 4:
            search_expenses()
        elif choice == 5:
            save_expenses()
        elif choice == 6:
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice!")

load_expenses()
main_menu()