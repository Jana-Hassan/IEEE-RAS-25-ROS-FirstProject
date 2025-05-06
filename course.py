from professor import Professor
from grading import Grading
from attendance import Attendance

class Course:
    def __init__(self, course_id, name, department, level, college, credit_hours):
        self.course_id = course_id
        self.name = name
        self.department = department
        self.level = level
        self.college = college
        self.credit_hours = credit_hours
        self.professors = []
        self.students = {}

    #add student to course in Admin mode    
    def add_student(self, student_id, student_name, student_level, student_college):
        self.is_enrolled = False
        if student_id in self.students:
            print(f"Student {student_name} is already enrolled in this course.")
            return
        
        if student_level != self.level:
            print(f"Student level ({student_level}) does not match course level.")
            return
        
        if student_college != self.college:
            print(f"Student college does not match course college ({self.college}).")
            return
        
        self.students[student_id] = {
            'name': student_name,
            'grade': None,
            'attendance': []
        }
        self.is_enrolled = True

    #remove student from course in Admin mode
    def remove_student(self, student_id):
        self.is_enrolled = False
        if student_id not in self.students:
            print(f"Student with ID {student_id} is not enrolled in this course.")
            return
        
        self.students.pop(student_id)
        self.is_enrolled = True

    #assign professor to course in Admin mode
    def assign_professor(self, professor):
        self.professor_assigned = False
        for p in self.professors:
            if p.professor_id == professor.professor_id:
                print(f"Professor {professor.name} is already assigned to this course.")
                return
        
        self.professors.append(professor)
        self.professor_assigned = True

    #remove professor from course in Admin mode
    def remove_professor(self, professor_id):
        self.professor_assigned = False
        for i, p in enumerate(self.professors):
            if p.professor_id == professor_id:
                self.professors.pop(i)
                self.professor_assigned = True
                return
        print(f"Professor with ID {professor_id} is not assigned to this course.")

    #get student info in Professor mode
    def get_student_info(self, student_id):
        self.is_enrolled = False
        if student_id not in self.students:
            print(f"Student with ID {student_id} is not enrolled in this course.")
            return None
        self.is_enrolled = True
        return self.students.get(student_id)

    def get_student_grade(self, student_id):
        return Grading().get_student_grade(self, student_id)

    def get_student_attendance(self, student_id):
        return Attendance().get_student_attendance(self, student_id)

    #convert course to dictionary
    def to_dict(self):
        return {
            'course_id': self.course_id,
            'name': self.name,
            'department': self.department,
            'level': self.level,
            'college': self.college,
            'credit_hours': self.credit_hours,
            'professors': [p.to_dict() for p in self.professors],
            'students': self.students
        }

    #convert dictionary to course
    @classmethod
    def from_dict(cls, data):
        course = cls(
            data['course_id'],
            data['name'],
            data['department'],
            data['level'],
            data['college'],
            data['credit_hours']
        )
        course.professors = [Professor.from_dict(p) for p in data['professors']]
        course.students = data['students']
        return course

    #print course info in Admin mode    
    def print_course_info(self):
        print(f"\nCourse ID: {self.course_id}")
        print(f"Name: {self.name}")
        print(f"Department: {self.department}")
        print(f"Level: {self.level}")
        print(f"College: {self.college}")
        print(f"Credit Hours: {self.credit_hours}")
        if self.professors:
            print("Professors:")
            for prof in self.professors:
                print(f"- {prof.name} (ID: {prof.professor_id})")
        else:
            print("No professors assigned to this course.")
        print(f"Number of students: {len(self.students)}") 

    #display available courses in two column table
    @staticmethod
    def display_available_courses(courses):
        if not courses:
            print("No courses available")
            return
        
        print("\nAvailable Courses:")
        print("-" * 50)
        print(f"{'Course ID'} {'Course Name'}")
        print("-" * 50)
        
        for course in courses:
            print(f"{course.course_id} {course.name}")