import students
import admin

admin.load_admin()

running = True

while running:
    if admin.login():
        students.load_students()

        while True:
            print("\nSTUDENT MANAGEMENT SYSTEM\n")
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Change Credentials")
            print("7. Logout")
            print("8. Exit")
            valid = True
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a number")
                valid = False

            if valid:

                if choice == 1:
                    students.add_student()

                elif choice == 2:
                    students.view_students()

                elif choice == 3:
                    students.search_student()

                elif choice == 4:
                    students.update_student()

                elif choice == 5:
                    students.delete_student()

                elif choice == 6:
                    admin.change_creds()

                elif choice == 7:
                    print("Logging out")
                    break

                elif choice == 8:
                    print("Exiting the program")
                    running = False
                    break

                else:
                    print("Please enter a valid choice")
