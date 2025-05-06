from course import Course
from student import Student
from professor import Professor

class Department:
    def __init__(self, dept_id, name, college):
    
        self.dept_id = dept_id
        self.name = name
        self.college = college
        self.courses = {}  
        self.students = {}  
        self.professors = {}  
      
    #add course to the department
    def add_course(self, course_id, name, level, credit_hours):
        if course_id in self.courses:
            print(f"Course {name} already exists")
            return False
        
        course = Course(course_id, name, self.name, level, self.college, credit_hours)
        self.courses[course_id] = course
        print(f"Course {name} added successfully")
        return True

    #remove course from the department
    def remove_course(self, course_id):
        if course_id not in self.courses:
            print(f"Course {course_id} not found")
            return False
        
        course_name = self.courses[course_id].name
        del self.courses[course_id]
        print(f"Course {course_name} removed successfully")
        return True

    
    def add_professor(self, prof_id, name, title):
        if prof_id in self.professors:
            print(f"Professor {name} already exists")
            return False
        
        professor = Professor(prof_id, name, self.name, self.college)
        self.professors[prof_id] = professor
        print(f"Professor {name} added successfully")
        return True

    def remove_professor(self, prof_id):
        if prof_id not in self.professors:
            print(f"Professor {prof_id} not found")
            return False
        
        prof_name = self.professors[prof_id].name
        del self.professors[prof_id]
        print(f"Professor {prof_name} removed successfully")
        return True

    def add_student(self, student):
        if student.student_id in self.students:
            print(f"Student {student.name} already exists")
            return False
            
        self.students[student.student_id] = student
        print(f"Student {student.name} added successfully")
        return True

    def print_department_info(self):
        print(f"\nDepartment: {self.name}")
        print(f"College: {self.college}")
        print(f"Number of Courses: {len(self.courses)}")
        print(f"Number of Students: {len(self.students)}")
        print(f"Number of Professors: {len(self.professors)}")
        
        print("\nCourses:")
        print("-" * 80)
        print(f"{'Course ID'} {'Name'} {'Level'} {'Credit Hours'}")
        print("-" * 80)
        
        for course in self.courses.values():
            print(f"{course.course_id} {course.name} {course.level} {course.credit_hours}")

    def to_dict(self):
        return {
            'dept_id': self.dept_id,
            'name': self.name,
            'college': self.college,
            'courses': {c_id: course.to_dict() for c_id, course in self.courses.items()},
            'students': {s_id: student.to_dict() for s_id, student in self.students.items()},
            'professors': {p_id: prof.to_dict() for p_id, prof in self.professors.items()}
        }

    @classmethod
    def from_dict(cls, data):
        department = cls(data['dept_id'], data['name'], data['college'])
        
        # Handle courses if they exist
        if 'courses' in data:
            for course_data in data['courses'].values():
                course = Course.from_dict(course_data)
                department.courses[course.course_id] = course
        
        # Handle students if they exist
        if 'students' in data:
            for student_data in data['students'].values():
                student = Student.from_dict(student_data)
                department.students[student.student_id] = student
        
        # Handle professors if they exist
        if 'professors' in data:
            for prof_data in data['professors'].values():
                professor = Professor.from_dict(prof_data)
                department.professors[professor.professor_id] = professor
        
        return department