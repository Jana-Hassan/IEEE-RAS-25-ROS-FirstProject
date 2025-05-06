import json
from grading import Grading
from attendance import Attendance
from registration import Registration

class Student:
    def __init__(self, student_id, name, level, college, department):
        self.student_id = student_id
        self.name = name
        self.level = level
        self.college = college
        self.department = department
        self.courses = {}
        self.registration = Registration()
        self.attendance = Attendance()
        self.grading = Grading()

    def register_course(self, course):
        return self.registration.register_course(self, course)

    def unregister_course(self, course_id):
        return self.registration.unregister_course(self, course_id)

    def get_grade(self, course_id):
        return self.grading.get_grade(self, course_id)

    def calculate_gpa(self):
        return self.grading.calculate_gpa(self)

    def track_attendance(self, course_id):
        return self.attendance.track_attendance(self, course_id)

    def get_student_info(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'department': self.department,
            'college': self.college,
            'level': self.level,
            'courses': self.courses
        }

    def print_courses(self):
        if not self.courses:
            print(f"\nStudent {self.name} is not enrolled in any courses.")
            return

        print(f"\nCourses for {self.name} (ID: {self.student_id}):")
        print("-" * 80)
        print(f"{'Course ID':<10} {'Course Name':<30} {'Grade':<8}")
        print("-" * 80)
        
        for course_id, course_info in self.courses.items():
            grade = course_info.get('grade', 'N/A')
            print(f"{course_id:<10} {course_info['name']:<30} {grade:<8}")

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'level': self.level,
            'college': self.college,
            'department': self.department,
            'courses': self.courses
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(
            data['student_id'],
            data['name'],
            data['level'],
            data['college'],
            data['department']
        )
        student.courses = data['courses']
        return student