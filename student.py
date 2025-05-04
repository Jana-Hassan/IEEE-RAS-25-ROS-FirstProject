from registration import register_course # Call the function
from course_data import course_db # Call the function


class Student:
    def __init__(self, id, name, college, level):
        self.id = id
        self.name = name
        self.college = college
        self.level = level
        self.courses = []
        self.grades = {}

    def register(self, course_id):
        register_course(self, course_id)

    def view_grades(self):
        if self.grades:
            for course, grade in self.grades.items():
                print(f"{course}: {grade}")
        else:
            print("No grades available.")


def main():
    print(" Welcome to the Student System ")
    student = None

    while not student:
        try:
            student_id = int(input("Enter your ID: "))
            student_name = input("Enter your name: ")

            if student_id in student_db and student_db[student_id][0] == student_name:
                college, level = student_db[student_id][1], student_db[student_id][2]
                student = Student(student_id, student_name, college, level)
                print(f"\nWelcome {student.name} from {student.college}, Level {student.level}.\n")
            else:
                print("Invalid ID or name. Please try again.\n")
        except ValueError:
            print("ID must be a number.\n")

    while True:
        print("\n1. Register for a course")
        print("2. View my grades")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            course_id = input("Enter course ID: ")
            student.register(course_id)  # Call the function
        elif choice == "2":
            student.view_grades()
        elif choice == "3":
            print("bye")
            break
        else:
            print("Invalid choice. Try again.")


main()
