from student import Student

class Grading:
    def assign_grade(student, course_id, grade):
        student.grade_assigned = False
    
        if not student:
            print("Student not found!")
            return
    
        if course_id not in student.courses:
            print(f"Student not enrolled in this course!")
            return
        
        student.courses[course_id]['grade'] = grade
        print(f"Grade {grade} assigned successfully for course {course_id}")
        student.grade_assigned = True


    def get_grade(student, course_id):
        student.grade_assigned = False

        if not student:
            print("Student not found!")
            return None
        
 
        if course_id not in student.courses:
            print(f"Student not enrolled in this course!")
            return None
        
        grade = student.courses[course_id]['grade']
        if grade is None:
            print(f"No grade assigned yet for this course.")
        else:
            student.grade_assigned = True
        return grade

    def calculate_gpa(student):
        student.grade_assigned = False
        
        if not student:
            print("Student not found!")
            return None
        
        total_hours = 0
        total_points = 0
        
        for course_id, course_info in student.courses.items():
            grade = course_info['grade']
            if grade is not None:
                hours = course_info['credit_hours']
                total_hours += hours
                total_points += grade * hours
        
        if total_hours == 0:
            print("No grades assigned to this course to calculate GPA")
            return None
        
        gpa = total_points / total_hours
        print(f"GPA: {gpa:.2f}")
        student.grade_assigned = True
        return gpa