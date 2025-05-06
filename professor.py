from grading import Grading
from attendance import Attendance
import json
from student import Student
from datetime import datetime

class Professor:
    def __init__(self, professor_id, name, department, college):
        self.professor_id = professor_id
        self.name = name
        self.department = department
        self.college = college
        self.courses = {}

    def assign_course(self, course_id, course_name):
        if course_id in self.courses:
            print(f"Professor {self.name} is already assigned to course {course_name}.")
            return False
        
        self.courses[course_id] = {
            'name': course_name
        }
        return True

    def remove_course(self, course_id):
        if course_id not in self.courses:
            print(f"Professor {self.name} is not assigned to course with ID {course_id}.")
            return False
        
        self.courses.pop(course_id)
        return True

    def assign_grade(self, course_id, student_id, grade):
        if course_id not in self.courses:
            print(f"Course {course_id} not found.")
            return False
        
        return Grading().assign_grade(self, course_id, student_id, grade)

    def mark_attendance(self, course_id, student_id, is_present):
        if course_id not in self.courses:
            print(f"Course {course_id} not found.")
            return False
        
        return Attendance().mark_attendance(self, course_id, student_id, is_present)

   

    

    def to_dict(self):
        return {
            'professor_id': self.professor_id,
            'name': self.name,
            'department': self.department,
            'college': self.college,
            'courses': self.courses
        }

    @classmethod
    def from_dict(cls, data):
        professor = cls(
            data['professor_id'],
            data['name'],
            data['department'],
            data['college']
        )
        professor.courses = data.get('courses', {})
        return professor