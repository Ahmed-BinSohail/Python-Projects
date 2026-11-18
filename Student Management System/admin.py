import json

admin_username = "admin"
admin_password = "admin123"

def login():
    print("\nADMIN LOGIN")
    attempts = 3
    while attempts > 0:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username == admin_username and password == admin_password:
            print("Login successful")
            return True
        else:
            attempts -= 1
            print("Invalid username or password")
            print("attempts left: ", attempts)
    print("Too many failed attempts. Access denied.")
    return False

def change_creds():
    global admin_username, admin_password
    print("\nADMIN CHANGE CREDENTIALS")
    new_username = input("Enter new username: ").strip()
    if  new_username == "":
        print("New username cannot be empty")
        return
    new_password = input("Enter new password: ").strip()
    if new_password == "":
        print("New password cannot be empty")
        return
    if len(new_password) < 6:
        print("password must be at least 6 characters")
        return
    confirm_password = input("Confirm new password: ").strip()
    if new_password != confirm_password:
        print("Passwords do not match")
        return
    try:
        with open("admin.json", "w") as file:
            json.dump({
                "username": new_username,
                "password": new_password
            }, file)
        print("Admin credentials changed")
        admin_username = new_username
        admin_password = new_password
    except OSError:
        print("Unable to save admin credentials")

def load_admin():
    global admin_username, admin_password
    try:
        with open("admin.json", "r") as file:
            data = json.load(file)
            admin_username = data["username"]
            admin_password = data["password"]
    except FileNotFoundError:
        print("Using default admin credentials")
    except json.JSONDecodeError:
        print("Admin credential file is invalid. Using default credentials")
    except KeyError:
        print("Admin credentials are incomplete. Using default credentials")