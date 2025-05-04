class Course:
    def __init__(self, course_id, name, department, level, college):
        self.course_id = course_id
        self.name = name
        self.department = department
        self.level = level
        self.college = college
        self.professors = []
        self.students = {}

    def add_student(self, student_id, student_name, student_level, student_college):
        if student_id in self.students:
            print(f"Student {student_name} (ID: {student_id}) is already enrolled in this course.")
            return False
        
        if student_level != self.level:
            print(f"Student level ({student_level}) does not match course level ({self.level}).")
            return False
        
        if student_college != self.college:
            print(f"Student college ({student_college}) does not match course college ({self.college}).")
            return False
        
        self.students[student_id] = {
            'name': student_name,
            'grade': None,
            'attendance': []
        }
        return True

    def remove_student(self, student_id):
        if student_id not in self.students:
            print(f"Student with ID {student_id} is not enrolled in this course.")
            return False
        
        self.students.pop(student_id)
        return True

    def assign_professor(self, professor_id, professor_name):
        for prof in self.professors:
            if prof['id'] == professor_id:
                print(f"Professor {professor_name} is already assigned to this course.")
                return False
        
        self.professors.append({
            'id': professor_id,
            'name': professor_name
        })
        return True

    def remove_professor(self, professor_id):
        for i, prof in enumerate(self.professors):
            if prof['id'] == professor_id:
                self.professors.pop(i)
                return True
        print(f"Professor with ID {professor_id} is not assigned to this course.")
        return False

    def add_grade(self, student_id, grade):
        if student_id not in self.students:
            print(f"Student with ID {student_id} is not enrolled in this course.")
            return False
        
        student = self.students[student_id]
        student['grade'] = grade
        return True

    def add_attendance(self, student_id, date, present):
        if student_id not in self.students:
            print(f"Student with ID {student_id} is not enrolled in this course.")
            return False
        
        student = self.students[student_id]
        student['attendance'].append({
            'date': date,
            'present': present
        })
        return True

    def get_student_info(self, student_id):
        if student_id not in self.students:
            print(f"Student with ID {student_id} is not enrolled in this course.")
            return None
        return self.students.get(student_id)

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'name': self.name,
            'department': self.department,
            'level': self.level,
            'college': self.college,
            'professors': self.professors,
            'students': self.students
        }

    @classmethod
    def from_dict(cls, data):
        course = cls(
            data['course_id'],
            data['name'],
            data['department'],
            data['level'],
            data['college']
        )
        course.professors = data['professors']
        course.students = data['students']
        return course

    def print_course_info(self):
        print(f"\nCourse ID: {self.course_id}")
        print(f"Name: {self.name}")
        print(f"Department: {self.department}")
        print(f"Level: {self.level}")
        print(f"College: {self.college}")
        if self.professors:
            print("Professors:")
            for prof in self.professors:
                print(f"- {prof['name']} (ID: {prof['id']})")
        else:
            print("No professors assigned to this course.")
        print(f"Number of students: {len(self.students)}")