class Registration:
    def register_course(self, student, course):
        self.registration_success = False
        
        if not student:
            print("Student not found!")
            return

        if course.course_id in student.courses:
            print(f"Already registered in {course.name}.")
            return

        if student.level < course.level:
            print(f"Cannot register for {course.name}. It requires level {course.level}.")
            return

        if len(student.courses) >= 7:
            print("Course limit reached. Max is 7.")
            return

        # Check if course belongs to student's department
        if course.department != student.department:
            print(f"Cannot register for {course.name}. Course belongs to different department.")
            return

        student.courses[course.course_id] = {
            'name': course.name,
            'credit_hours': course.credit_hours,
            'grade': None
        }
        print(f"Course {course.name} registered successfully.")
        self.registration_success = True

    def unregister_course(self, student, course):
        self.registration_success = False
        
        if not student:
            print("Student not found!")
            return

        if course.course_id not in student.courses:
            print(f"Not registered in {course.name}.")
            return

        del student.courses[course.course_id]
        print(f"Successfully unregistered from {course.name}")
        self.registration_success = True