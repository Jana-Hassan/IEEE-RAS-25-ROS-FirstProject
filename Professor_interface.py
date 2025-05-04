
# professor_interface.py

from professor import Professor
from course import Course

def professor_menu(professor, courses):
    while True:
        print("\n====== Professor Menu ======")
        print("1. View My Courses")
        print("2. Assign Grade")
        print("3. Mark Attendance")
        print("4. View Student Info")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            professor.print_professor_info()

        elif choice == '2':
            course_id = input("Enter course ID: ")
            student_id = input("Enter student ID: ")
            grade = float(input("Enter grade: "))

            course = find_course_by_id(courses, course_id)
            if course:
                professor.add_grade(course, student_id, grade)
            else:
                print("Course not found.")

        elif choice == '3':
            course_id = input("Enter course ID: ")
            student_id = input("Enter student ID: ")
            date = input("Enter date (YYYY-MM-DD): ")
            status = input("Is the student present? (y/n): ").lower() == 'y'

            course = find_course_by_id(courses, course_id)
            if course:
                professor.mark_attendance(course, student_id, date, status)
            else:
                print("Course not found.")

        elif choice == '4':
            course_id = input("Enter course ID: ")
            student_id = input("Enter student ID: ")

            course = find_course_by_id(courses, course_id)
            if course:
                info = course.get_student_info(student_id)
                if info:
                    print(f"\nStudent Info: {info}")
            else:
                print("Course not found.")

        elif choice == '5':
            print("Exiting professor menu. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


def find_course_by_id(courses, course_id):
    for course in courses:
        if course.course_id == course_id:
            return course
    return None


if __name__ == "__main__":
    c1 = Course("CS101", "Intro to CS", "CS", 1, "Engineering")
    c1.add_student("S001", "Ali", 1, "Engineering")

    p1 = Professor("P001", "Dr. Ahmed", "CS", "Engineering")
    p1.assign_course(c1)

    courses = [c1]

    professor_menu(p1, courses)
