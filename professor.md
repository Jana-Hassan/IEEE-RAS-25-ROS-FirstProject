```python

# professor.py

class Professor:
    def __init__(self, professor_id, name, department, college):
        self.professor_id = professor_id
        self.name = name
        self.department = department
        self.college = college
        self.courses = []  

    def assign_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            course.assign_professor(self.professor_id, self.name)
            print(f"{self.name} assigned to course {course.name}")
        else:
            print(f"{self.name} is already assigned to course {course.name}")

    def add_grade(self, course, student_id, grade):
        success = course.add_grade(student_id, grade)
        if success:
            print(f"Grade {grade} added for student {student_id} in course {course.name}")
        else:
            print(f"Failed to add grade for student {student_id} in course {course.name}")

    def mark_attendance(self, course, student_id, date, present=True):
        success = course.add_attendance(student_id, date, present)
        if success:
            status = "present" if present else "absent"
            print(f"Marked {status} for student {student_id} on {date} in course {course.name}")
        else:
            print(f"Failed to mark attendance for student {student_id} in course {course.name}")

    def print_professor_info(self):
        print(f"\nProfessor ID: {self.professor_id}")
        print(f"Name: {self.name}")
        print(f"Department: {self.department}")
        print(f"College: {self.college}")
        print(f"Assigned Courses:")
        for course in self.courses:
            print(f"- {course.name} (ID: {course.course_id})")
