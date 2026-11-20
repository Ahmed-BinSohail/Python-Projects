import json

contacts = []

print("Welcome to Contact Book!")

def load_contacts():
    try:
        with open("contacts.json", "r") as file:
            data = json.load(file)
            contacts.extend(data)
    except FileNotFoundError:
        print("No contacts saved!")
    except json.JSONDecodeError:
        print("Contact file is corrupted!")

def save_contacts():
    with open("contacts.json", "w") as file:
        json.dump(contacts, file)

def add_contact():
    name = input("Enter contact name: ").strip()
    number = input("Enter contact number: ").strip()
    if number == "":
        print("Contact number cannot be empty!")
    if name == "" or number == "":
        print("Name and number cannot be empty!")
        return
    for contact in contacts:
        if contact["number"] == number:
            print("This number already exists!")
            return
    contact = {
        "name": name,
        "number": number
    }
    contacts.append(contact)
    save_contacts()
    print("Contact added!")

def view_contacts():
    if contacts == []:
        print("No contacts added!")
    else:
        for i, contact in enumerate(contacts, start=1):
            print(f'\n{i}. Name: {contact["name"]}\nNumber: {contact["number"]}')

def search_contact():
    contact_name = input("Enter contact name: ").strip()
    found = False
    for i, contact in enumerate(contacts, start=1):
        if contact["name"].upper() == contact_name.upper():
            found = True
            print(f"{i}. Name: {contact['name']}, number: {contact['number']}")
    if not found:
        print("Contact not found!")

def update_contact():
    name = input("Enter contact name: ").strip()
    found = False
    for contact in contacts:
        if contact["name"].upper() == name.upper():
            found = True
            new_number = input("Enter new contact number: ").strip()
            for c in contacts:
                if c["number"] == new_number and c != contact:
                    print("This number already belongs to another contact!")
                    return
            contact["number"] = new_number
            save_contacts()
            print("Contact updated!")
            break
    if not found:
        print("Contact not found!")

def delete_contact():
    name = input("Enter contact name: ").strip()
    found = False
    for contact in contacts:
        if contact["name"].upper() == name.upper():
            found = True
            contacts.remove(contact)
            save_contacts()
            print("Contact deleted!")
            break
    if not found:
        print("Contact not found!")

def main_menu():
    while True:
        print("====CONTACT BOOK====")
        print("1. Add contact\n2. View contact\n3. Search contact\n4. Update contact\n5. Delete contact\n6. Exit\n")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                add_contact()
            elif choice == 2:
                view_contacts()
            elif choice == 3:
                search_contact()
            elif choice == 4:
                update_contact()
            elif choice == 5:
                delete_contact()
            elif choice == 6:
                print("Program Ended!")
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a numeric value!")

load_contacts()
main_menu()

