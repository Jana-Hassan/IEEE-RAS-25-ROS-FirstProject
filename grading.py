from config import GRADE_SCALE

class Grading:

    #assign grade to a student in Professor mode
    def assign_grade(self, student, course_id, grade):
        self.grade_assigned = False
        if not student:
            print("Student not found.")
            return

        if course_id not in student.courses:
            print(f"You are not enrolled in this course.")
            return
  
        student.courses[course_id]['grade'] = grade
        print(f"Grade {grade} assigned successfully")
        student.grade_assigned = True

    #get grade of a student in student Mode
    def get_grade(self, student, course_id):
        self.grade_assigned = False
        if not student:
            print("Student not found!")
            return None

        if course_id not in student.courses:
            print(f"You are not enrolled in this course!")
            return None

        grade = student.courses[course_id].get('grade')
        if grade is None:
            print(f"No grade assigned yet for you.")
            return None

        self.grade_assigned = True
        return grade
    
    #calculate GPA of a student in student Mode
    def calculate_gpa(self, student):
        self.grade_assigned = False
        if not student or not student.courses:
            print("No courses found for you.")
            return 0.0

        total_points = 0
        total_hours = 0

        for course_id, course_info in student.courses.items():
            grade = course_info.get('grade')
            if grade is not None:
                hours = course_info['credit_hours']
                points = GRADE_SCALE.get(grade, 0.0)  # Get points for grade from config
                total_hours += hours
                total_points += points * hours
        
        if total_hours == 0:
            print("No grades assigned to this course to calculate GPA")
            return None
        
        gpa = total_points / total_hours
        print(f"GPA: {gpa:.2f}")
        student.grade_assigned = True
        return gpa