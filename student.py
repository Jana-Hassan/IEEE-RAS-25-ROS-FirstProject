#database
student_db = {
    101: ("name 1", "Engineering", 2),
    102: ("name 2", "Medicine", 3),
    103: ("name 3", "Business", 1)
}

course_db = {
    "Math101": 1,
    "Physics201": 2,
    "Surgery301": 3,
    "Finance101": 1,
    "Control202": 2,

}


class Student:
    def __init__(self, id, name, college, level):
        self.id = id
        self.name = name
        self.college = college
        self.level = level
        self.courses = []
        self.grades = {}

    def register_course(self, course_id):
        if course_id not in course_db:
            print("Invalid course.")
        required_level = course_db[course_id]
        if self.level < required_level:
            print(f"Cannot register for {course_id}. It requires level {required_level}.")
            return

        if len(self.courses) >= 7:
            print("Course limit reached. Max is 7.")
            return

        if course_id in self.courses:
            print(f"Already registered in {course_id}.")
        else:
            self.courses.append(course_id)
            print(f"Course {course_id} registered successfully.")

    def view_grades(self):
        if self.grades:
            for course, grade in self.grades.items():
                print(f"{course}: {grade}")
        else:
            print("No grades available.")


#  Main page

def main():
    print(" Welcome to the Student System ")
    student = None

    # registration first
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
            student.register_course(course_id)
        elif choice == "2":
            student.view_grades()
        elif choice == "3":
            print("bye")
            break
        else:
            print("Invalid choice. Try again.")

main()