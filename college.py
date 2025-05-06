from course import Course
from student import Student
from department import Department
from grading import Grading

class College:
    def __init__(self, college_id, name):
        self.college_id = college_id
        self.name = name
        self.departments = {}
        self.students = {}

    def add_department(self, dept_id, name):
        if dept_id in self.departments:
            print(f"Department {name} already exists.")
            return False
        
        department = Department(dept_id, name, self.name)
        self.departments[dept_id] = department
        return True

  

    def available_courses(self):
        available_courses = []
        for department in self.departments.values():
            for course in department.courses.values():
                available_courses.append({
                    'id': course.course_id,
                    'name': course.name,
                    'department': department.name,
                    'level': course.level,
                    'credit_hours': course.credit_hours
                })
        return available_courses

    def print_students(self):
        if not self.students:
            print(f"\nNo students registered in {self.name}.")
            return

        print(f"\nCollege: {self.name}")
        print("\nStudents:")
        print("-" * 50)
        print(f"{'Student ID'} {'Name'} {'Level'}")
        print("-" * 50)
        
        for student in self.students.values():
            print(f"{student.student_id} {student.name} {student.department} {student.leve}")

    def to_dict(self):
        return {
            'college_id': self.college_id,
            'name': self.name,
            'departments': {dept_id: dept.to_dict() for dept_id, dept in self.departments.items()},
            'students': {student_id: student.to_dict() for student_id, student in self.students.items()}
        }

    @classmethod
    def from_dict(cls, data):
        college = cls(data['college_id'], data['name'])
        
        # Handle departments if they exist
        if 'departments' in data:
            for dept_data in data['departments'].values():
                department = Department.from_dict(dept_data)
                college.departments[department.dept_id] = department
        
        # Handle students if they exist
        if 'students' in data:
            for student_data in data['students'].values():
                student = Student.from_dict(student_data)
                college.students[student.student_id] = student
        
        return college