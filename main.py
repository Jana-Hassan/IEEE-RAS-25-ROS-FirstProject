import json
from config import (
    DATA_FILE, MAIN_MENU, STUDENT_MENU, PROFESSOR_MENU, ADMIN_MENU,
    COLLEGES, DEPARTMENTS, COURSE_LEVELS, GRADE_SCALE
)
from student import Student
from course import Course
from professor import Professor
from college import College
from datetime import datetime

class BaseInterface:
    def __init__(self, data):
        self.data = data
        
#save data to json file
    def save_data(self):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

#display data as table
    def display_table(self, headers, data, title=None):
        if title:
            print(f"\n{title}")
        
        # Calculate column widths
        col_widths = [len(str(header)) for header in headers]
        for row in data:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Create format string
        format_str = " | ".join(f"{{:<{width}}}" for width in col_widths)
        
        # Print header
        print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
        print(format_str.format(*headers))
        print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        
        # Print data
        for row in data:
            print(format_str.format(*row))
        print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))

    #display menu 
    def display_menu(self, menu):
        print("\n" + "="*50)
        for key, value in menu.items():
            print(f"{key}. {value}")
        print("="*50)

    def get_input(self, prompt, valid_options=None):
        while True:
            choice = input(prompt).strip()
            if valid_options is None or choice in valid_options:
                return choice
            print(f"Invalid input! Try again.")

    #post operation menu
    def post_operation_menu(self, operation_name):
        print(f"\n{operation_name} completed successfully!")
        print("\n[1] Perform another operation.. | [2] Back to previous menu.. | [0] Exit system..\n")
        
        choice = self.get_input("Enter your choice: ", ['0', '1', '2'])
        return choice

class StudentInterface(BaseInterface):
    def __init__(self, data):
        super().__init__(data)

    def register_course(self, student_id):
        student_data = self.data['students'][student_id]
        student = Student.from_dict(student_data)
        
        # Display available courses for student's level and department
        available_courses = [
            [course_id, course['name'], course['level'], course['credit_hours']]
            for course_id, course in self.data['courses'].items()
            if (course['level'] == student.level and 
                course['department'] == student.department and
                course_id not in student.courses)
        ]
        
        if not available_courses:
            print("No available courses for your level and department!")
            return False
        
        self.display_table(["ID", "Course Name", "Level", "Credit Hours"], 
                          available_courses, "Available Courses")
        
        course_id = self.get_input("Enter course ID to register: ", 
                                 [course[0] for course in available_courses])
        
        course_data = self.data['courses'][course_id]
        course = Course(
            course_id=course_id,
            name=course_data['name'],
            level=course_data['level'],
            department=course_data['department'],
            college=course_data['college'],
            credit_hours=course_data['credit_hours']
        )
        
        if student.register_course(course):
            # Update student's courses in data
            self.data['students'][student_id] = student.to_dict()
            
            # Add student to course's students list
            self.data['courses'][course_id]['students'][student_id] = {
                'name': student.name,
                'grade': None,
                'attendance': {}  # Initialize attendance as empty dictionary
            }
            
            self.save_data()
            return True
        return False

    def view_grades(self, student_id):
        student_data = self.data['students'][student_id]
        student = Student.from_dict(student_data)
        student.print_courses()
        return True

    def view_attendance(self, student_id):
        student_data = self.data['students'][student_id]
        student = Student.from_dict(student_data)
        
        if not student.courses:
            print("You are not enrolled in any courses!")
            return False
        
        course_data = [[course_id, course_info['name']] 
                      for course_id, course_info in student.courses.items()]
        self.display_table(["ID", "Course Name"], course_data, "Your Courses")
        
        course_id = self.get_input("Enter course ID to view attendance: ", 
                                 student.courses.keys())
        
        attendance = student.track_attendance(course_id)
        if attendance:
            attendance_data = []
            for record in attendance:
                status = "Present" if record['present'] else "Absent"
                attendance_data.append([record['date'], status])
            
            self.display_table(
                ["Date", "Status"],
                attendance_data,
                f"Attendance for {student.courses[course_id]['name']}"
            )
            return True
        return False

    def calculate_gpa(self, student_id):
        student_data = self.data['students'][student_id]
        student = Student.from_dict(student_data)
        return student.calculate_gpa() is not None

    def run(self):
        print("\nStudent Interface")
        print("Enter your ID to continue...")
        student_id = input("Student ID: ")
        
        if student_id not in self.data['students']:
            print("Student not found!")
            return
        
        student = self.data['students'][student_id]
        print(f"\nWelcome, {student['name']}!")
        
        while True:
            self.display_menu(STUDENT_MENU)
            choice = self.get_input("Enter your choice: ", STUDENT_MENU.keys())
            
            if choice == "0":
                break
            elif choice == "1":
                if self.register_course(student_id):
                    next_action = self.post_operation_menu("Course Registration")
                    if next_action == "0":  
                        break
                    elif next_action == "2":  
                        continue
            elif choice == "2":
                if self.view_grades(student_id):
                    next_action = self.post_operation_menu("View Grades")
                    if next_action == "0":  
                        break
                    elif next_action == "2":  
                        continue
            elif choice == "3":
                if self.view_attendance(student_id):
                    next_action = self.post_operation_menu("Track Attendance")
                    if next_action == "0":  
                        break
                    elif next_action == "2": 
                        continue
            elif choice == "4":
                if self.calculate_gpa(student_id):
                    next_action = self.post_operation_menu("Calculate GPA")
                    if next_action == "0":  
                        break
                    elif next_action == "2": 
                        continue

class ProfessorInterface(BaseInterface):
    def __init__(self, data):
        super().__init__(data)

    def get_professor_courses(self, prof_id):
        return [
            course_id for course_id, course in self.data['courses'].items()
            if (course.get('professor_id') == prof_id or 
                any(p.get('professor_id') == prof_id for p in course.get('professors', [])))
        ]

    def assign_grade(self, prof_id):
        """Assign grade to a student"""
        professor = Professor.from_dict(self.data['professors'][prof_id])
        
        # Get professor's courses
        prof_courses = self.get_professor_courses(prof_id)
        
        if not prof_courses:
            print("You are not assigned to any courses!")
            return False
        
        # Display professor's courses
        course_data = [[course_id, self.data['courses'][course_id]['name']] 
                      for course_id in prof_courses]
        self.display_table(["ID", "Course Name"], course_data, "Your Courses")
        
        course_id = self.get_input("Enter course ID: ", prof_courses)
        course = self.data['courses'][course_id]
        
        if not course['students']:
            print("No students enrolled in this course!")
            return False
        
        # Display enrolled students
        student_data = [[student_id, student['name']] 
                       for student_id, student in course['students'].items()]
        self.display_table(["ID", "Student Name"], student_data, "Enrolled Students")
        
        student_id = self.get_input("Enter student ID: ", course['students'].keys())
        
        # Display available grades
        grade_data = [[grade, f"{grade} ({points})"] 
                     for grade, points in GRADE_SCALE.items()]
        self.display_table(["Grade", "Points"], grade_data, "Available Grades")
        
        grade = self.get_input("Enter grade: ", GRADE_SCALE.keys())
        
        # Use Professor's assign_grade method
        if professor.assign_grade(course_id, student_id, grade):
            # Update data
            self.data['courses'][course_id]['students'][student_id]['grade'] = grade
            self.data['students'][student_id]['courses'][course_id]['grade'] = grade
            self.save_data()
            return True
        return False

    def mark_attendance(self, prof_id):
        professor = Professor.from_dict(self.data['professors'][prof_id])
        
        # Get professor's courses
        prof_courses = self.get_professor_courses(prof_id)
        
        if not prof_courses:
            print("You are not assigned to any courses!")
            return False
        
        # Display professor's courses
        course_data = [[course_id, self.data['courses'][course_id]['name']] 
                      for course_id in prof_courses]
        self.display_table(["ID", "Course Name"], course_data, "Your Courses")
        
        course_id = self.get_input("Enter course ID: ", prof_courses)
        course = self.data['courses'][course_id]
        
        if not course['students']:
            print("No students enrolled in this course!")
            return False
        
        # Display enrolled students
        student_data = [[student_id, student['name']] 
                       for student_id, student in course['students'].items()]
        self.display_table(["ID", "Student Name"], student_data, "Enrolled Students")
        
        student_id = self.get_input("Enter student ID: ", course['students'].keys())
        
        # Mark attendance
        status = self.get_input("Enter status (present/absent): ", ['present', 'absent'])
        
        # Use Professor's mark_attendance method
        if professor.mark_attendance(course_id, student_id, status == 'present'):
            # Reload data after professor updates it
            with open(DATA_FILE, 'r') as f:
                self.data = json.load(f)
            return True
        return False

    def view_course_students(self, prof_id):
        professor = Professor.from_dict(self.data['professors'][prof_id])
        
        # Get professor's courses
        prof_courses = self.get_professor_courses(prof_id)
        
        if not prof_courses:
            print("You are not assigned to any courses!")
            return False
        
        # Display professor's courses
        course_data = [[course_id, self.data['courses'][course_id]['name']] 
                      for course_id in prof_courses]
        self.display_table(["ID", "Course Name"], course_data, "Your Courses")
        
        course_id = self.get_input("Enter course ID: ", prof_courses)
        course = self.data['courses'][course_id]
        
        if not course['students']:
            print("No students enrolled in this course!")
            return False
        
        student_data = []
        for student_id, student_info in course['students'].items():
            grade = student_info.get('grade', 'N/A')
            attendance_records = student_info.get('attendance', [])
            total_classes = len(attendance_records)
            present = sum(1 for record in attendance_records if record.get('present', False))
            attendance_rate = (present / total_classes * 100) if total_classes > 0 else 0
            
            student_data.append([
                student_id,
                student_info['name'],
                grade,
                f"{present}/{total_classes}",
                f"{attendance_rate:.1f}%"
            ])
        
        self.display_table(
            ["ID", "Name", "Grade", "Attendance", "Rate"],
            student_data,
            f"Students in {course['name']}"
        )
        return True

    def run(self):
        print("\nProfessor Interface")
        print("Please enter your professor ID to continue...")
        prof_id = input("Professor ID: ")
        
        if prof_id not in self.data['professors']:
            print("Professor not found!")
            return
        
        professor = self.data['professors'][prof_id]
        print(f"\nWelcome, {professor['name']}!")
        
        while True:
            self.display_menu(PROFESSOR_MENU)
            choice = self.get_input("Enter your choice: ", PROFESSOR_MENU.keys())
            
            if choice == "0":
                break
            elif choice == "1":
                if self.assign_grade(prof_id):
                    next_action = self.post_operation_menu("Assign Grade")
                    if next_action == "0":  
                        break
                    elif next_action == "2":  
                        continue
            elif choice == "2":
                if self.mark_attendance(prof_id):
                    next_action = self.post_operation_menu("Mark Attendance")
                    if next_action == "0": 
                        break
                    elif next_action == "2":  
                        continue
            elif choice == "3":
                if self.view_course_students(prof_id):
                    next_action = self.post_operation_menu("View Course Students")
                    if next_action == "0":  
                        break
                    elif next_action == "2":  
                        continue

class AdminInterface(BaseInterface):
    def __init__(self, data):
        super().__init__(data)

    def add_student(self):
        """Add a new student"""
        print("\nAdd New Student")
        student_id = input("Enter student ID: ")
        
        if student_id in self.data['students']:
            print("Error: Student ID already exists!")
            return False
        
        name = input("Enter student name: ")
        
        # Display available colleges
        college_data = [[college_id, college_name] for college_name, college_id in COLLEGES.items()]
        self.display_table(["ID", "College Name"], college_data, "Available Colleges")
        college_id = self.get_input("Enter college ID: ", COLLEGES.values())
        college_name = next(name for name, id in COLLEGES.items() if id == college_id)
        
        # Display available departments for selected college
        dept_data = [[dept_id, dept_name] for dept_name, dept_id in DEPARTMENTS[college_name].items()]
        self.display_table(["ID", "Department Name"], dept_data, f"Available Departments in {college_name}")
        dept_id = self.get_input("Enter department ID: ", DEPARTMENTS[college_name].values())
        dept_name = next(name for name, id in DEPARTMENTS[college_name].items() if id == dept_id)
        
        # Display available levels
        level_data = [[str(i), f"Level {i}"] for i in range(1, 5)]
        self.display_table(["ID", "Level"], level_data, "Available Levels")
        level = self.get_input("Enter level ID: ", [str(i) for i in range(1, 5)])
        
        # Get or create department
        if college_name not in self.data['colleges']:
            self.data['colleges'][college_name] = College(college_id, college_name).to_dict()
        
        college = College.from_dict(self.data['colleges'][college_name])
        if dept_id not in college.departments:
            college.add_department(dept_id, dept_name)
        
        department = college.departments[dept_id]
        
        # Use Department's add_student method
        student = Student(student_id, name, level, college_name, dept_name)
        if department.add_student(student):
            # Update data
            self.data['students'][student_id] = student.to_dict()
            self.data['colleges'][college_name] = college.to_dict()
            self.save_data()
            return True
        return False

    def add_professor(self):
        """Add a new professor"""
        print("\nAdd New Professor")
        prof_id = input("Enter professor ID: ")
        
        if prof_id in self.data['professors']:
            print("Error: Professor ID already exists!")
            return False
        
        name = input("Enter professor name: ")
        
        # Display available colleges
        college_data = [[college_id, college_name] for college_name, college_id in COLLEGES.items()]
        self.display_table(["ID", "College Name"], college_data, "Available Colleges")
        college_id = self.get_input("Enter college ID: ", COLLEGES.values())
        college_name = next(name for name, id in COLLEGES.items() if id == college_id)
        
        # Display available departments for selected college
        dept_data = [[dept_id, dept_name] for dept_name, dept_id in DEPARTMENTS[college_name].items()]
        self.display_table(["ID", "Department Name"], dept_data, f"Available Departments in {college_name}")
        dept_id = self.get_input("Enter department ID: ", DEPARTMENTS[college_name].values())
        dept_name = next(name for name, id in DEPARTMENTS[college_name].items() if id == dept_id)
        
        # Get or create department
        if college_name not in self.data['colleges']:
            self.data['colleges'][college_name] = College(college_id, college_name).to_dict()
        
        college = College.from_dict(self.data['colleges'][college_name])
        if dept_id not in college.departments:
            college.add_department(dept_id, dept_name)
        
        department = college.departments[dept_id]
        
        # Use Department's add_professor method
        if department.add_professor(prof_id, name, "Professor"):
            # Update data
            self.data['professors'][prof_id] = {
                'professor_id': prof_id,
                'name': name,
                'college': college_name,
                'department': dept_name,
                'courses': {}
            }
            self.data['colleges'][college_name] = college.to_dict()
            self.save_data()
            return True
        return False

    def add_course(self):
        """Add a new course"""
        print("\nAdd New Course")
        course_id = input("Enter course ID: ")
        
        if course_id in self.data['courses']:
            print("Error: Course ID already exists!")
            return False
        
        name = input("Enter course name: ")
        
        # Display available colleges
        college_data = [[college_id, college_name] for college_name, college_id in COLLEGES.items()]
        self.display_table(["ID", "College Name"], college_data, "Available Colleges")
        college_id = self.get_input("Enter college ID: ", COLLEGES.values())
        college_name = next(name for name, id in COLLEGES.items() if id == college_id)
        
        # Display available departments for selected college
        dept_data = [[dept_id, dept_name] for dept_name, dept_id in DEPARTMENTS[college_name].items()]
        self.display_table(["ID", "Department Name"], dept_data, f"Available Departments in {college_name}")
        dept_id = self.get_input("Enter department ID: ", DEPARTMENTS[college_name].values())
        dept_name = next(name for name, id in DEPARTMENTS[college_name].items() if id == dept_id)
        
        # Display available levels
        level_data = [[str(i), f"Level {i}"] for i in range(1, 5)]
        self.display_table(["ID", "Level"], level_data, "Available Levels")
        level = self.get_input("Enter level ID: ", [str(i) for i in range(1, 5)])
        
        credit_hours = int(self.get_input("Enter credit hours: ", ['2', '3', '4', '5']))
        
        # Get or create department
        if college_name not in self.data['colleges']:
            self.data['colleges'][college_name] = College(college_id, college_name).to_dict()
        
        college = College.from_dict(self.data['colleges'][college_name])
        if dept_id not in college.departments:
            college.add_department(dept_id, dept_name)
        
        department = college.departments[dept_id]
        
        # Use Department's add_course method
        if department.add_course(course_id, name, level, credit_hours):
            # Update data
            course = department.courses[course_id]
            self.data['courses'][course_id] = course.to_dict()
            self.data['colleges'][college_name] = college.to_dict()
            self.save_data()
            return True
        return False

    def remove_student(self):
        # Display available students
        student_data = [[student_id, student['name'], student['college'], student['department']] 
                      for student_id, student in self.data['students'].items()]
        self.display_table(["ID", "Name", "College", "Department"], student_data, "Available Students")
        student_id = self.get_input("Enter student ID to remove: ", self.data['students'].keys())
        
        # Confirm removal
        confirm = self.get_input(f"Are you sure you want to remove student {student_id}? (y/n): ", ['y', 'n'])
        if confirm == 'y':
            student_data = self.data['students'][student_id]
            college_name = student_data['college']
            dept_name = student_data['department']
            
            # Get department
            college = College.from_dict(self.data['colleges'][college_name])
            department = college.departments[dept_name]
            
            # Remove student from all enrolled courses
            for course_id in list(student_data['courses'].keys()):
                if course_id in department.courses:
                    course = department.courses[course_id]
                    course.remove_student(student_id)
                    self.data['courses'][course_id] = course.to_dict()
            
            # Remove student from department
            if student_id in department.students:
                del department.students[student_id]
            
            # Remove student from system
            del self.data['students'][student_id]
            self.data['colleges'][college_name] = college.to_dict()
            self.save_data()
            return True
        return False

    def remove_professor(self):
        """Remove a professor"""
        # Display available professors
        prof_data = [[prof_id, prof['name'], prof['college'], prof['department']] 
                   for prof_id, prof in self.data['professors'].items()]
        self.display_table(["ID", "Name", "College", "Department"], prof_data, "Available Professors")
        prof_id = self.get_input("Enter professor ID to remove: ", self.data['professors'].keys())
        
        # Confirm removal
        confirm = self.get_input(f"Are you sure you want to remove professor {prof_id}? (y/n): ", ['y', 'n'])
        if confirm == 'y':
            professor_data = self.data['professors'][prof_id]
            college_name = professor_data['college']
            dept_name = professor_data['department']
            
            # Get department ID from department name
            # First find the correct college name from COLLEGES
            actual_college_name = next(cname for cname in COLLEGES.keys() 
                                    if college_name.replace("College of ", "").strip() == cname)
            dept_id = next(id for name, id in DEPARTMENTS[actual_college_name].items() 
                         if name == dept_name)
            
            # Get department
            college = College.from_dict(self.data['colleges'][actual_college_name])
            if dept_id not in college.departments:
                print(f"Department {dept_name} not found in {actual_college_name}!")
                return False
                
            department = college.departments[dept_id]
            
            # Remove professor from all assigned courses
            for course_id in list(professor_data['courses'].keys()):
                if course_id in department.courses:
                    course = department.courses[course_id]
                    course.remove_professor(prof_id)
                    self.data['courses'][course_id] = course.to_dict()
            
            # Remove professor from department
            if prof_id in department.professors:
                del department.professors[prof_id]
            
            # Remove professor from system
            del self.data['professors'][prof_id]
            self.data['colleges'][actual_college_name] = college.to_dict()
            self.save_data()
            return True
        return False

    def remove_course(self):
        """Remove a course"""
        # Display available courses
        course_data = [[course_id, course['name'], course['department']] 
                     for course_id, course in self.data['courses'].items()]
        self.display_table(["ID", "Course Name", "Department"], course_data, "Available Courses")
        course_id = self.get_input("Enter course ID to remove: ", self.data['courses'].keys())
        
        # Confirm removal
        confirm = self.get_input(f"Are you sure you want to remove course {course_id}? (y/n): ", ['y', 'n'])
        if confirm == 'y':
            course_data = self.data['courses'][course_id]
            college_name = course_data['college']
            dept_name = course_data['department']
            
            # Get the actual college name without prefix
            actual_college_name = next(cname for cname in COLLEGES.keys() 
                                    if college_name.replace("College of ", "").strip() == cname)
            dept_id = next(id for name, id in DEPARTMENTS[actual_college_name].items() 
                         if name == dept_name)
            
            # Get department
            college = College.from_dict(self.data['colleges'][actual_college_name])
            department = college.departments[dept_id]
            
            # Use Department's remove_course method
            if department.remove_course(course_id):
                # Remove course from system
                del self.data['courses'][course_id]
                self.data['colleges'][actual_college_name] = college.to_dict()
                self.save_data()
                return True
        return False

    def run(self):
        """Handle admin interface"""
        print("\nAdmin Interface")
        while True:
            self.display_menu(ADMIN_MENU)
            choice = self.get_input("Enter your choice: ", ADMIN_MENU.keys())
            
            if choice == "0":
                break
            elif choice == "1":  # Add Student
                if self.add_student():
                    next_action = self.post_operation_menu("Student Addition")
                    if next_action == "0":  # Exit
                        return
                    elif next_action == "2":  # Back to admin menu
                        continue
            elif choice == "2":  # Add Professor
                if self.add_professor():
                    next_action = self.post_operation_menu("Professor Addition")
                    if next_action == "0":  # Exit
                        return
                    elif next_action == "2":  # Back to admin menu
                        continue
            elif choice == "3":  # Add Course
                if self.add_course():
                    next_action = self.post_operation_menu("Course Addition")
                    if next_action == "0":  # Exit
                        return
                    elif next_action == "2":  # Back to admin menu
                        continue
            elif choice == "4":  # Remove Student
                if self.remove_student():
                    next_action = self.post_operation_menu("Student Removal")
                    if next_action == "0":  # Exit
                        return
                    elif next_action == "2":  # Back to admin menu
                        continue
            elif choice == "5":  # Remove Professor
                if self.remove_professor():
                    next_action = self.post_operation_menu("Professor Removal")
                    if next_action == "0":  # Exit
                        return
                    elif next_action == "2":  # Back to admin menu
                        continue
            elif choice == "6":  # Remove Course
                if self.remove_course():
                    next_action = self.post_operation_menu("Course Removal")
                    if next_action == "0":  # Exit
                        return
                    elif next_action == "2":  # Back to admin menu
                        continue

class CLI:
    def __init__(self):
        self.data = self.load_data()
        if not self.data:
            print("Could not load data. Starting with empty system.")
            self.data = {
                'students': {},
                'professors': {},
                'courses': {},
                'colleges': {}
            }
        self.student_interface = StudentInterface(self.data)
        self.professor_interface = ProfessorInterface(self.data)
        self.admin_interface = AdminInterface(self.data)

    def load_data(self):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {DATA_FILE} not found")
            return None
        except json.JSONDecodeError:
            print(f"Error: {DATA_FILE} is not valid JSON")
            return None

    def run(self):
        print("Welcome to University Management System!")
        
        while True:
            self.admin_interface.display_menu(MAIN_MENU)
            choice = self.admin_interface.get_input("Enter your choice: ", MAIN_MENU.keys())
            
            if choice == "0":
                print("\nThank you for using the system!")
                break
            elif choice == "1":
                self.student_interface.run()
            elif choice == "2":
                self.professor_interface.run()
            elif choice == "3":
                self.admin_interface.run()

if __name__ == "__main__":
    cli = CLI()
    cli.run()