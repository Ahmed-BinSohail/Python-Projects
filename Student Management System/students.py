import json

students = []

def load_students():
    students.clear()
    try:
        with open("students.json") as file:
            data = json.load(file)
            if not isinstance(data, list):
                print("Invalid student data format")
                return

        for student in data:
            if not isinstance(student, dict):
                print("Invalid student record")
                return
            if "id" not in student:
                print("Invalid student record")
                return
            if "name" not in student:
                print("Invalid student record")
                return
            if "age" not in student:
                print("Invalid student record")
                return
            if "course" not in student:
                print("Invalid student record")
                return
            if not isinstance(student['id'], int) or isinstance(student['id'], bool):
                print("Invalid student record")
                return
            if not isinstance(student['name'], str):
                print("Invalid student record")
                return
            if not isinstance(student['age'], int) or isinstance(student['age'], bool):
                print("Invalid student record")
                return
            if not isinstance(student['course'], str):
                print("Invalid student record")
                return
            students.append(student)

    except FileNotFoundError:
        print("Previously registered students not found")
    except json.JSONDecodeError:
        print("Student record file is empty or invalid")

def save_students():
    try:
        with open("students.json", "w") as file:
            json.dump(students, file)
            return True
    except OSError:
        print("Unable to save student records")
        return False

def view_students():
    print("2. View Students selected")

    if not students:
        print("No students registered")

    else:
        for student in students:
            print("ID:", student["id"])
            print("Name:", student["name"])
            print("Age:", student["age"])
            print("Course:", student["course"])

def search_student():
    print("3. Search Student selected")
    valid = True
    try:
        find_student = int(input("Enter student ID: "))
    except ValueError:
        print("Student ID must be an integer")
        valid = False
    if valid:
        found = False
        for student in students:
            if student["id"] == find_student:
                found = True
                print("ID:", student["id"])
                print("Name:", student["name"])
                print("Age:", student["age"])
                print("Course:", student["course"])
                break

        if not found:
            print("Student not found")

def add_student():
    print("1. Add Student selected")

    valid = True

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Student ID must be an integer")
        valid = False

    if valid:
        exist = False

        for student in students:
            if student["id"] == student_id:
                exist = True
                print("ID already exists")
                break

        if not exist:
            student_name = input("Enter student name: ").strip()
            if student_name == "":
                print("Student name cannot be empty")
                valid = False
        if valid:
            try:
                student_age = int(input("Enter student age: "))
                if student_age <= 0:
                    print("Student age must be greater than 0")
                    valid = False
            except ValueError:
                print("Student age must be an integer")
                valid = False

            if valid:
                student_course = input("Enter student course: ").strip()
                if student_course == "":
                    print("Student course cannot be empty")
                    valid = False
            if valid:
                std = {
                    "id": student_id,
                    "name": student_name,
                    "age": student_age,
                    "course": student_course
                }

                students.append(std)
                if save_students():
                    print("Student added successfully")
                else:
                    students.pop()

def update_student():
    print("4. Update Student selected")
    valid = True
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Student ID must be an integer")
        valid = False
    if valid:
        found = False

        for student in students:
            if student["id"] == student_id:
                found = True
                old_student = student.copy()
                print("Enter new student details:")
                student_name = input("Enter student name: ").strip()
                if student_name == "":
                    print("Student name cannot be empty")
                    valid = False
                if valid:
                    try:
                        student_age = int(input("Enter student age: "))
                        if student_age <= 0:
                            print("Student age must be greater than 0")
                            valid = False
                    except ValueError:
                        print("Student age must be an integer")
                        valid = False
                if valid:
                    student_course = input("Enter student course: ").strip()
                    if student_course == "":
                        print("Student course cannot be empty")
                        valid = False
                if valid:
                    student["age"] = student_age
                    student["course"] = student_course
                    student["name"] = student_name
                    if save_students():
                        print("Student updated successfully")
                    else:
                        student.update(old_student)
                    break

        if not found:
            print("Student not found")

def delete_student():
    print("5. Delete Student selected")
    valid = True
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Student ID must be an integer")
        valid = False
    if valid:
        found = False
        for student in students:
            if student["id"] == student_id:
                found = True
                index = students.index(student)
                students.remove(student)
                if save_students():
                    print("Student removed successfully")
                else:
                    students.insert(index, student)
                break

        if not found:
            print("Student not found")